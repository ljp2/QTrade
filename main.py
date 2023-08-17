import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import api

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
BARS_DIRECTORY = f'{parent_directory}/BARS'



def initial_bars(ticker:str, number_days:int=1):
    dd = timedelta(days=1)
    day = datetime.today()
    target_length = number_days * 389
    bars = pd.DataFrame()
    num_attmepts = 0

    while num_attmepts < 5:
        num_attmepts += 1
        try:
            df = api.get_minute_bars_for_day(ticker=ticker, day=day)
            print( "About to concat len = ", len(df))
            bars = pd.concat([bars, df])
        except:
            pass
        if len(bars) < target_length:
            day = day - dd
        else:
            break
        print(num_attmepts, '\t', len(bars))
    if len(bars) < target_length:
        raise RuntimeError("Could not initialize required number of minute bars")
    bars.sort_index(inplace=True)
    return bars

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
        plt.addItem(pg.PlotDataItem(x=[pos, pos],y=[row.low, row.high],pen=pg.mkPen(color, width=3)))
        plt.addItem(pg.BarGraphItem(x=index, y0=bot, y1=top, width=0.5, brush=color))

    
# df = initial_bars('SPY')

# app = pg.mkQApp()
# mw = QtWidgets.QMainWindow()
# mw.setWindowTitle('pyqtgraph example: PlotWidget')
# mw.resize(800,800)
# cw = QtWidgets.QWidget()
# mw.setCentralWidget(cw)
# l = QtWidgets.QVBoxLayout()
# cw.setLayout(l)

# pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
# l.addWidget(pw)
# pw2 = pg.PlotWidget(name='Plot2')
# l.addWidget(pw2)
# pw3 = pg.PlotWidget()
# l.addWidget(pw3)

# mw.show()

# # plotCandles(pw, df)

# pg.exec()

# bars = initial_bars('SPY')
# print('len =', len(bars))
# print(bars.head())
# print(bars.tail())
# bars.to_csv("bars.csv")