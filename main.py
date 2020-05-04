from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
from pandas.plotting import register_matplotlib_converters
from pandas import pandas as pd

from instruments.Stock import Stock
from instruments.Portfolio import Portfolio
import constants as C


class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui", self)

        self.setWindowTitle("Stock Analysis")
     
        self.pushButton_generate_graph.clicked.connect(self.make_plot)

        self.addToolBar(NavigationToolbar(self.MainWidget.canvas, self))
        self.addToolBar(NavigationToolbar(self.RSIWidget.canvas, self))
        self.addToolBar(NavigationToolbar(self.VolumeWidget.canvas, self))

    def make_plot(self):
        symbol = self.symbol_in.text()
        name = self.name_in.text()
        start = self.start_in.date().toString("yyyy-MM-dd")
        end = self.end_in.date().toString("yyyy-MM-dd")
        stock = Stock(symbol, C.BASE_DIR, name, start, end)
        self.plot_main(stock)
        self.plot_rsi(stock)
        self.plot_volume(stock)

    def plot_volume(self, stock):
        df = stock.stock_df
        register_matplotlib_converters()
        x = pd.to_datetime(df['date'])
        
        y_volume = df['adjVolume']

        self.VolumeWidget.canvas.axes.clear()
        self.VolumeWidget.canvas.axes.plot(x, y_volume)
        self.VolumeWidget.canvas.axes.set_ylabel('Adj Volume', fontsize=9)
        self.VolumeWidget.canvas.axes.grid()
        self.VolumeWidget.canvas.draw()

    def plot_rsi(self, stock):
        df = stock.stock_df
        register_matplotlib_converters()
        x = pd.to_datetime(df['date'])
        
        y_rsi = df['rsi14']

        self.RSIWidget.canvas.axes.clear()
        self.RSIWidget.canvas.axes.plot(x, y_rsi)
        self.RSIWidget.canvas.axes.set_ylim([0, 100])
        self.RSIWidget.canvas.axes.set_ylabel('RSI', fontsize=9)
        self.RSIWidget.canvas.axes.grid()
        self.RSIWidget.canvas.draw()

    def plot_main(self, stock):

            df = stock.stock_df
            register_matplotlib_converters()
            x = pd.to_datetime(df['date'])
            
            y_close = df['adjClose']
            # y_short = df['sma12']
            y_long = df['sma26']
            y_upr = df['uprBol']
            y_lwr = df['lwrBol']

            self .MainWidget.canvas.axes . clear () 
            self.MainWidget.canvas.axes.plot(x, y_close, label='Adj Close')
            # self.MainWidget.canvas.axes.plot(x, y_short, label='Short-Term Simple Moving Avg')
            self.MainWidget.canvas.axes.plot(x, y_long, label='Long-Term Simple Moving Avg')
            self.MainWidget.canvas.axes.plot(x, y_lwr, label="Lower Bollinger")
            self.MainWidget.canvas.axes.plot(x, y_upr, label="Upper Bollinger")
            self.MainWidget.canvas.axes.set_ylabel('Price', fontsize=9)
            self.MainWidget.canvas.axes.set_title(stock.symbol + ": " + stock.name)
            self.MainWidget.canvas.axes.legend()
            self.MainWidget.canvas.axes.grid()
            self.MainWidget.canvas.draw()

app = QApplication([]) 
window = MatplotlibWidget() 
window.show() 
app.exec_()