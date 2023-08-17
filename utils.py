import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def read_saved_bars():
    df = pd.read_csv('bars.csv', header=0, index_col=0)
    return df


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


def combine(xf:pd.DataFrame):
    res =  {
        'index':xf.index[0],
        'open':xf.iloc[0].open,
        'high':xf.high.max(),
        'low':xf.low.min(),
        'close':xf.iloc[-1].close
    }
    return res

def condense_bars(df:pd.DataFrame, number_of_bars:int):
    N = len(df)
    nlast = N 
    nfirst = N - number_of_bars

    z = df.iloc[range(nfirst, nlast)]
    
    xf = combine(z)
    return xf


df = read_saved_bars()

print(df.tail())

xf = condense_bars(df,5)

print(xf)
