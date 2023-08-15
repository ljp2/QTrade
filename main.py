import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import api

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
BARS_DIRECTORY = f'{parent_directory}/BARS'

print('BARS DIRECTORY =', BARS_DIRECTORY)


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



bars = initial_bars('SPY')
print('len =', len(bars))
print(bars.head())
print(bars.tail())
bars.to_csv("bars.csv")