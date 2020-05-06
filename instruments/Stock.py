import re
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from instruments.Instrument import Instrument
import constants as C
import pandas as pd
import pandas_datareader
import numpy as np
import os


# TODO: Parameterize this class
class Stock(Instrument):

    def __init__(self, symbol, path, name, start_date, end_date):
        # Constructor
        super(Stock, self).__init__(name, start_date, end_date)
        self.symbol = symbol
        self.path = f"{path}{self.symbol}.csv"
        self.download_data()
        self.stock_df = pd.read_csv(self.get_path())
        self.calc_sma(12)
        self.calc_sma(26)
        self.calc_smstd(12)
        self.calc_smstd(26)
        self.calc_rsi(14)
        self.calc_bollinger(26, 2)

    def download_data(self):
        # Downloads and stores stock data in a CSV file
        if os.path.exists(C.BASE_DIR):
            pass
        else:
            os.makedirs(C.BASE_DIR)
        temp_df = pandas_datareader.tiingo.TiingoDailyReader(self.symbol, start=self.start_date, end=self.end_date,
                                                             retry_count=3,
                                                             pause=0.1, timeout=30, session=None, freq=None,
                                                             api_key=C.TIINGO_API_KEY).read()
        temp_df.to_csv(self.get_path())

    def update_csv(self):
        # Updates CSV data file with current stock_df
        os.remove(self.get_path())
        self.stock_df.to_csv(self.get_path())

    def calc_sma(self, period):
        # Computes the moving average given a period and stores in the CSV
        self.stock_df[f"sma{period}"] = self.stock_df["adjClose"]
        self.stock_df[f"sma{period}"] = self.stock_df[f"sma{period}"].rolling(window=period,
                                                                              center=False).mean()
        self.update_csv()

    def calc_smstd(self, period):
        # Computes the moving standard deviation given a period and stores in the CSV
        self.stock_df[f"smstd{period}"] = self.stock_df["adjClose"]
        self.stock_df[f"smstd{period}"] = self.stock_df[f"smstd{period}"].rolling(window=period,
                                                                                  center=False).std()
        self.update_csv()

    def calc_bollinger(self, period, deviations_away):
        upr_std = self.stock_df[f"smstd{period}"].apply(lambda x: x * deviations_away)
        self.stock_df['uprBol'] = self.stock_df[f"sma{period}"].add(upr_std, fill_value=0)
        upr_std = self.stock_df[f"smstd{period}"].apply(lambda x: x * deviations_away)
        self.stock_df['lwrBol'] = self.stock_df[f"sma{period}"].sub(upr_std, fill_value=0)
        self.update_csv()

    # TODO: TEST AND CONFIRM CORRECTNESS
    def calc_rsi(self, period):
        # Computes the relative strength index (rsi) for a given period and stores in the CSV
        # backtested on QQQ data
        # get delta, separate first row
        __delta = self.stock_df["adjClose"].diff()
        __tr = __delta[0:1]
        __delta = __delta.dropna()
        # split delta into gains vs losses
        __u, __d = __delta * 0, __delta * 0
        __u[__delta > 0] = __delta[__delta > 0]
        __d[__delta < 0] = -__delta[__delta < 0]
        # set the first mean
        __u.iloc[period - 1] = np.mean(__u[:period])
        __d.iloc[period - 1] = np.mean(__d[:period])
        # separate NaNs from data
        __u[0:period - 1] = np.nan
        __u_to_add = __u[0:period - 1]
        __u = __u[period - 1:]
        __d = __d[period - 1:]
        # calculate rsi
        __rs = __u.ewm(com=period - 1, adjust=False).mean() / \
            __d.ewm(com=period - 1, adjust=False).mean()
        __rsi = 100.0 - 100.0 / (1.0 + __rs)
        __rsi = __rsi.to_frame()
        # reshape data frame to include original NaN's
        __rsi = pd.concat([__tr, __u_to_add, __rsi])
        __rsi = __rsi.rename(columns={"adjClose": "rsi"})
        self.stock_df[f"rsi{period}"] = __rsi["rsi"]
        self.update_csv()

    def cut_df(self):
        # Cuts the data frame to the longest lag period and updates the csv to eliminate leading NaNs
        all_lagging_cats = []
        lag_periods = []
        for col in self.stock_df.columns:
            if ("sma" in col or "smstd" in col or "rsi" in col):
                all_lagging_cats.append(col)
        for cat in all_lagging_cats:
            lag_periods.append(int((re.findall(r"\d+", cat))[0]))
        largest_lag = max(lag_periods)
        if largest_lag != 0:
            largest_lag = largest_lag - 1
        self.stock_df = self.stock_df[largest_lag:]
        self.update_csv()

    def plot_basic(self):

        # Define data series
        df = self.stock_df
        register_matplotlib_converters()
        x = pd.to_datetime(df['date'])
        y_close = df['adjClose']
        # y_short = df['sma12']
        y_long = df['sma26']
        y_upr = df['uprBol']
        y_lwr = df['lwrBol']
        y_rsi = df['rsi14']
        y_volume = df['adjVolume']

        # Create subplots
        fig, (main, rsi, volume) = plt.subplots(
            3, 1, gridspec_kw={'height_ratios': [5, 1, 1]})

        # Main graph
        main.plot(x, y_close, label='Adj Close')
        # main.plot(x, y_short, label='Short-Term Simple Moving Avg')
        main.plot(x, y_long, label='Long-Term Simple Moving Avg')
        main.plot(x, y_upr, label="Upper Bollinger")
        main.plot(x, y_lwr, label="Lower Bollinger")
        main.set_ylabel('Price', fontsize=9)
        main.set_title(self.symbol + ": " + self.name)
        main.legend()
        main.grid()

        # RSI graph
        rsi.plot(x, y_rsi)
        rsi.set_ylim([0, 100])
        rsi.set_ylabel('RSI', fontsize=9)
        rsi.grid()

        # Volume graph
        volume.plot(x, y_volume)
        volume.set_ylabel('Adj Volume', fontsize=9)
        volume.grid()
        # fig.tight_layout()
        plt.show()


#   def get_dt(self, str):
#        return dt.datetime(int(str[0:4]), int(str[5:7]), int(str[8:10]))
