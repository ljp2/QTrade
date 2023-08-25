import pandas as pd
from datetime import datetime, timedelta
from myapi import get_minute_bars_day_open_hours
from time import sleep

dd = timedelta(days = 1)

day = datetime.now()
n = 0
while n < 30:
    df = get_minute_bars_day_open_hours('SPY', day)
    if len(df) > 0:
        day_str = day.strftime('%b-%d')
        print(day_str)
        df.to_csv(f'Bars/{day_str}.csv')
        n += 1
        sleep(0.5)
    day = day - dd
