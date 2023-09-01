import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

import plot

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
BARS_DIRECTORY = f'{parent_directory}/BARS'

class Bars:
    def __init__(self, barsfile:str) -> None:
       self.df = pd.read_csv(f'./Bars/{barsfile}',header=0, index_col='timestamp')
       self.start = 0
       self.end = len(self.df)
       
       
    def next(self, num = 1):
        end = self.start + num
        if end > self.end:
            end = self.end
        if self.start <= end:
            if num == 1:
                result = self.df.iloc[[self.start]]
            else:
                result = self.df.iloc[self.start:end]
            self.start += num
            return result
        else:
            raise StopIteration


# bars = Bars('Aug-26.csv')
df = pd.read_csv('Bars/Aug-26.csv',header=0, index_col='timestamp')
xf = df.iloc[-50:]

app = pg.mkQApp("DateAxisItem Example")

# w = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})


# plotCandles(w, xf)

# w.showGrid(x=True, y=True)

# w.show()

w = plot.PlotLayout()
plot.plotCandles(w.p1, xf)

w.show()

if __name__ == '__main__':
    pg.exec()