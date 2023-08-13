import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import myapi

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
BARS_DIRECTORY = f'{parent_directory}/BARS'

print('BARS DIRECTORY =', BARS_DIRECTORY)


def trade(ticker:str):
    setup_bars(ticker)

def setup_bars(ticker:str):
    pass

bars = myapi.get_minute_bars('SPY')
print('len =', len(bars))
print(bars.head())
print(bars.tail())
bars.to_csv("bars.csv")