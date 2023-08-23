import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import myapi

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
BARS_DIRECTORY = f'{parent_directory}/BARS'


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


# today = datetime.now()
# df = myapi.get_minute_bars_day_open_hours('SPY', today)
# df.to_csv('bars.csv')

df = pd.read_csv('bars.csv',header=0, index_col='timestamp')

app = pg.mkQApp("DateAxisItem Example")

w = pg.PlotWidget(axisItems = {'bottom': pg.DateAxisItem()})
w.resize(1200, 800)

plotCandles(w, df)

w.showGrid(x=True, y=True)

w.show()

if __name__ == '__main__':
    pg.exec()