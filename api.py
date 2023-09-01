import os
import pandas as pd
from time import sleep
from datetime import datetime, time, timedelta
import pytz
eastern_timezone = pytz.timezone('America/New_York')


from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.common.types import RawData
from alpaca.data import Quote, Trade, Snapshot, Bar
from alpaca.trading.models import TradeAccount, Position, ClosePositionResponse
from alpaca.trading.requests import GetAssetsRequest, GetOrdersRequest, MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import AssetClass, OrderSide, QueryOrderStatus, TimeInForce
from alpaca.trading.client import TradingClient


from keys import paper_apikey, paper_secretkey, live_apikey, live_secretkey


stock_hist_client = StockHistoricalDataClient(paper_apikey, paper_secretkey)
trading_client = TradingClient(paper_apikey, paper_secretkey)
live_trading_client = TradingClient(live_apikey, live_secretkey, paper=False)

def isDST(date:datetime):
    return eastern_timezone.localize(date).dst() != timedelta(0)

def filter_open_hours(df:pd.DataFrame) -> pd.DataFrame:
    start_time = '09:30:00'
    end_time = '15:59:00'
    return df.between_time(start_time, end_time)


def get_lastest_quote_single(ticker:str) -> RawData:
    request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker)
    latest_quote = stock_hist_client.get_stock_latest_quote(request_params=request_params)
    x = latest_quote[ticker]
    return x
    
def get_lastest_quote_multiple(tickers:list[str]) -> dict[str, Quote]:
    multisymbol_request_params  = StockLatestQuoteRequest(symbol_or_symbols=tickers)
    latest_quote = stock_hist_client.get_stock_latest_quote(request_params=multisymbol_request_params)
    return latest_quote


def get_minute_bars_for_today_open(ticker:str):
    now = datetime.now()
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Minute,
        start =  datetime(now.year, now.month, now.day),
        end = None
    )
    try:
        df = stock_hist_client.get_stock_bars(request_params).df.loc[ticker]
        df.index = df.index.tz_convert(eastern_timezone)
        df = filter_open_hours(df)
        df.index = df.index.astype('int64') // 10**9
    except:
        return None
    if len(df) > 0:
        return df
    else:
        return None


def get_minute_bars_for_day_open(ticker:str, day:datetime):
    e = datetime(day.year, day.month, day.day)
    s = e - timedelta(days=1)
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Minute,
        start = s,
        end = e
    )
    try:
        df = stock_hist_client.get_stock_bars(request_params).df.loc[ticker]
        df.index = df.index.tz_convert(eastern_timezone)
        df = filter_open_hours(df)
        df.index = df.index.astype('int64') // 10**9
    except:
        return None
    if len(df) > 0:
        return df
    else:
        return None

def get_minute_bars_for_day(ticker:str, day:datetime):
    s = datetime(day.year, day.month, day.day)
    e = s - timedelta(days=1)
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Minute,
        start = s,
        end = e
    )
    try:
        df = stock_hist_client.get_stock_bars(request_params).df.loc[ticker]
    except:
        df = None
    return df


def get_historical_data_utc(ticker:str, number_days= 1, timeframe:TimeFrame = TimeFrame.Minute ) -> pd.DataFrame:
    today = datetime.today()
    dd = timedelta(days=1)
    if today.time() < time(18, 0):
        startday = today.date() - dd
    else:
        startday = today.date()
    startday = startday - number_days * dd
    request_params = StockBarsRequest(
        symbol_or_symbols='SPY',
        timeframe=timeframe,
        start=startday.strftime("%Y-%m-%d 00:00")
        # start=startday.strftime("%Y-%m-%d 14:30")
    )       
    bars = stock_hist_client.get_stock_bars(request_params)
    df = bars.df.loc[ticker]
    df.index = df.index.tz_convert(eastern_timezone)
    return filter_open_hours(df)


def get_account_details(is_paper:bool=True) -> TradeAccount:
    if is_paper:
        account = trading_client.get_account()
    else:
     account = live_trading_client.get_account()
    return account

def get_all_assets():
    search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
    assets = trading_client.get_all_assets(search_params)
    return assets
    

def get_all_orders(side=None):
    request_params = GetOrdersRequest(
                    status=QueryOrderStatus.OPEN,
                 )
    orders = trading_client.get_orders(filter=request_params)
    return orders

def cancel_all_orders():
    cancel_statuses = trading_client.cancel_orders()
    return cancel_statuses


def get_all_positions() -> list[Position]:
    positions = trading_client.get_all_positions()
    return positions

def close_all_positions() ->  list[ClosePositionResponse]:
    response = trading_client.close_all_positions(cancel_orders=True)
    return response


def place_market_order_(symbol, qty, notational, side, time_in_force ):
    if (qty is not None) and (notational is None):
        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side=side,
                            time_in_force=time_in_force
        )
    elif (qty is None) and (notational is not None):
        market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        notational = notational,
                        side=side,
                        time_in_force=time_in_force
        )
    else:
        raise Exception
    market_order = trading_client.submit_order(
                    order_data=market_order_data
    )
    return market_order


def place_limit_order_(symbol, limit_price, qty, side, time_in_force ):
    limit_order_data = LimitOrderRequest(
                        symbol=symbol,
                        limit_price=limit_price,
                        qty=qty,
                        side=side,
                        time_in_force=time_in_force
    )
    limit_order = trading_client.submit_order(
                    order_data=limit_order_data
    )
    return limit_order 

    
def BUY_market_order_qty(symbol:str, qty:float, time_in_force=TimeInForce.DAY ):
    market_order = place_market_order_(symbol, qty=qty, notational=None, side=OrderSide.BUY, time_in_force=time_in_force)
    return market_order
    
def BUY_market_order_notational(symbol:str, notational:float, time_in_force=TimeInForce.DAY ):
    market_order = place_market_order_(symbol,  qty=None, notational=notational, side=OrderSide.BUY, time_in_force=time_in_force)
    return market_order
    
def SELL_market_order_qty(symbol:str, qty:float, time_in_force=TimeInForce.DAY ):
    market_order = place_market_order_(symbol, qty=qty, notational=None, side=OrderSide.SELL, time_in_force=time_in_force)
    return market_order

def SELL_market_order_notational(symbol:str, notational:float, time_in_force=TimeInForce.DAY ):
    market_order = place_market_order_(symbol,  qty=None, notational=notational, side=OrderSide.SELL, time_in_force=time_in_force)
    return market_order

def BUY_limit_order(symbol:str, limit_price:float, qty:float, time_in_force=TimeInForce.DAY ):
    limit_order = place_limit_order_(symbol, limit_price=limit_price, qty=qty, side=OrderSide.BUY, time_in_force=time_in_force)
    return limit_order

def SELL_limit_order(symbol:str, limit_price:float, qty:float, time_in_force=TimeInForce.DAY ):
    limit_order = place_limit_order_(symbol, limit_price=limit_price, qty=qty, side=OrderSide.SELL, time_in_force=time_in_force)
    return limit_order
