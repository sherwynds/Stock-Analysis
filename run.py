from instruments.Stock import Stock
from instruments.Portfolio import Portfolio
import constants as C

# OBSOLETE LEGACY


# spy = Stock("SPY", "S&P 500", '1990-01-01', '2019-01-01')
# spy.cut_df()

# apple = Stock("AAPL", "Apple", '1990-01-01', '2019-01-01')
# apple.cut_df()

TSLA = Stock("TSLA", C.BASE_DIR, "Tesla", "2015-01-01", '2019-01-01')
print(TSLA.stock_df.head(26))
#AAPL.cut_df()
# my_pf = Portfolio({"TSLA": [0.2], "MSFT": [0.8]}, C.BASE_DIR, "My Porftfolio", "2015-01-01", "2019-01-01")
# print(my_pf.instruments.get("TSLA")[1].stock_df.head(26))
# my_pf.instruments.get("TSLA")[1].cut_df()
# print(my_pf.instruments.get("TSLA")[1].stock_df["adjClose"].head(25))
TSLA.plot_basic()

# import pandas as pd
#
# df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
# df = df.rename(columns={"A": "testCol"})
# print(df)
