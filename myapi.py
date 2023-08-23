import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import api
import pytz
eastern_timezone = pytz.timezone('America/New_York')


def get_minute_bars_day_open_hours(ticker:str, day:datetime):
    """
    returned DataFrame has unix timestamp as index
    """
    df = pd.DataFrame()
    try:
        df = api.get_minute_bars_for_day(ticker=ticker, day=day)
    except:
        pass
    if len(df) > 0:
        df.index = df.index.tz_convert(eastern_timezone)
        df = api.filter_open_hours(df)
        df.index = df.index.astype(int) // 10**9
    return df



# def get_minute_bars_open_hrs(ticker:str, number_days:int=2):
#     dd = timedelta(days=1)
#     day = datetime.today()
#     target_length = number_days * 389
#     bars = pd.DataFrame()
#     num_attmepts = 0
#     while num_attmepts < 5:
#         num_attmepts += 1
#         try:
#             df = api.get_minute_bars_for_day(ticker=ticker, day=day)
#             bars = pd.concat([bars, df])
#         except:
#             pass
#         if len(bars) < target_length:
#             day = day - dd
#         else:
#             break
#         print(num_attmepts, '\t', len(bars))
#     if len(bars) < target_length:
#         raise RuntimeError("Could not initialize required number of minute bars")
#     bars.sort_index(inplace=True)
#     return bars


