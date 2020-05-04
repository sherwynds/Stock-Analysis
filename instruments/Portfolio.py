# Contains a Name, Symbol, dictionary of stocks and weights
import os
import shutil

from instruments.Instrument import Instrument
import constants as C
from instruments.Stock import Stock


class Portfolio(Instrument):

    def __init__(self, instruments, path, name, start_date, end_date):
        super(Portfolio, self).__init__(name, start_date, end_date)
        self.instruments = instruments  # python dictionary "stock": weight (weights not strictly checked)
        self.instruments["SPY"] = [0]
        self.path = f"{path}{self.name}/"
        self.download_data()

    def download_data(self):
        # downloads data for all required stocks
        if self.is_saved():
            print("overwriting saved portfolio")
            shutil.rmtree(self.get_path(), ignore_errors=False, onerror=True)
        os.mkdir(self.path)
        for i, v in self.instruments.items():
            inst = Stock(i, self.get_path(), f"{self.name}: {i}", self.start_date, self.end_date)
            v.append(inst)


    # # TODO: Merge should take all the csv's / weights and create summary csv
    # def merge(self):
    #     columns = ["adjClose"]
    #     primary_df = self.ins
    #     for col in columns:
    #         for i,v in self.instruments.items():
    #             temp_df =
    #             self.ge
    #
    # def get_weighted_col(self, col, weight, inst):
    #     for
