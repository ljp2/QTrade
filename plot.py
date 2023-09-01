import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets


class PlotLayout():
    def __init__(self):
        self.w = pg.GraphicsLayoutWidget()
        self.p1 = self.w.addPlot(row=0, col=0)
        self.p2 = self.w.addPlot(row=1, col=0)
        self.p3 = self.w.addPlot(row=2, col=0)
        self.p1.setAxisItems({'bottom': pg.DateAxisItem()})
        self.p2.setAxisItems({'bottom': pg.DateAxisItem()})
        self.p3.setAxisItems({'bottom': pg.DateAxisItem()})

        self.p2.setXLink(self.p1)
        self.p3.setXLink(self.p1)


    def show(self):
        self.w.show()

    
def plotCandles(plt:pg.PlotItem, df:pd.DataFrame):
    for index,row in df.iterrows():
        color = 'g' if row.close > row.open else 'r'
        pos = index
        if row.close >= row.open:
            top = row.close 
            bot = row.open 
            color = 'g'
        else:
            top = row.open 
            bot = row.close
            color = 'r'
        plt.addItem(pg.PlotDataItem(x=[pos, pos],y=[row.low, row.high],pen=pg.mkPen(color, width=5)))
        plt.addItem(pg.BarGraphItem(x=index, y0=bot, y1=top, width=40, brush=color))


