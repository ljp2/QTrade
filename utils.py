#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


df = pd.read_csv('bars.csv', header=0, index_col=0)


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

print(df.tail())

xf = condense_bars(df,5)

print(xf)
