import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import api

def get_minute_bars(ticker:str, number_days:int=2):
    dd = timedelta(days=1)
    day = datetime.today()
    target_length = number_days * 389
    bars = pd.DataFrame()
    num_attmepts = 0
    while num_attmepts < 5:
        num_attmepts += 1
        try:
            df = api.get_minute_bars_for_day(ticker=ticker, day=day)
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


