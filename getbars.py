import pandas as pd
from datetime import datetime, timedelta
from time import sleep
from api import get_minute_bars_for_day_open, get_minute_bars_for_today_open

dd = timedelta(days = 1)
n = 0
target_n = 5
day = datetime.now()

ticker = "SPY"

df = get_minute_bars_for_today_open(ticker=ticker)
if (df is not None ) and (len(df) > 0):
    day_str = day.strftime('%b-%d')
    print(day_str)
    df.to_csv(f'Bars/{day_str}.csv')
    n += 1
sleep(0.5)

day = day - dd
while n < target_n:
    df = get_minute_bars_for_day_open(ticker=ticker, day=day)
    if (df is not None ) and (len(df) > 0):
        day_str = day.strftime('%b-%d')
        print(day_str)
        df.to_csv(f'Bars/{day_str}.csv')
        n += 1
    sleep(0.5)
    day = day - dd
