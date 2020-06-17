from __future__ import absolute_import, unicode_literals
from celery import task


@task()
def get_exchanges_day_data(exchange_symbol):
    """
    Method that iterates through an exchange and all of its listed stocks
    and runs the stock_tasks get_day_stock_data method to get the day data
    for that stock.
    :param exchange_symbol: Exchange symbol to get stocks for
    """
    from fintrack_be.models import Exchange, Stock
    from fintrack_be.tasks.stock_tasks import get_day_stock_data

    exchange = Exchange.objects.get(symbol=exchange_symbol)
    stocks = Stock.objects.filter(exchange=exchange).order_by('ticker')

    for stock in stocks:
        get_day_stock_data(stock.ticker)


@task()
def bulk_get_exchanges_day_data(exchange_symbol):
    """
    Method that gets a specific exchanges listed stocks day price data and
    creates them in bulk
    :param exchange_symbol: Exchange symbol to get data for
    """
    from fintrack_be.models import Exchange, Stock
    from fintrack_be.tasks.stock_tasks import get_bulk_day_stock_data

    exchange = Exchange.objects.get(symbol=exchange_symbol)
    stocks = Stock.objects.filter(exchange=exchange).order_by('ticker')

    for stock in stocks:
        get_bulk_day_stock_data(stock.ticker)


"""
These are exchange tasks that are responsible for getting 
the exchange stocks prices minute data, these are currently 
used
"""


@task()
def get_latest_data_for_open_markets():
    """
    Task that gets the latest price data for Stocks in Exchanges that are
    in trading hours.
    """
    from fintrack_be.models import Exchange, Stock
    from fintrack_be.tasks.stock_tasks import get_latest_stock_data

    exchanges = Exchange.objects.all().order_by('symbol')
    for exchange in exchanges:
        if exchange.market_open():
            stocks = Stock.objects.filter(exchange=exchange)
            for stock in stocks:
                get_latest_stock_data.delay(stock.ticker)


@task()
def get_exchanges_minute_data(exchange_symbol):
    """
    Method that iterates through an exchange and all of its listed stocks
    and runs the stock_tasks get_day_stock_data method to get the minute data
    for that stock.
    :param exchange_symbol: Exchange symbol to get stocks for
    """
    from fintrack_be.models import Exchange, Stock
    from fintrack_be.functions.stock.stock_data import get_stock_data, stock_price_data_df_to_model

    exchange = Exchange.objects.get(symbol=exchange_symbol)
    stocks = Stock.objects.filter(exchange=exchange)

    for stock in stocks:
        df = get_stock_data(ticker=stock.ticker, period='1d', interval='1m')
        stock_price_data_df_to_model(df)
        print('Added {} minute data')


@task()
def bulk_get_exchanges_minute_data(exchange_symbol):
    """
    Method that gets a specific exchanges listed stocks minute price data and
    creates them in bulk
    :param exchange_symbol: Exchange symbol to get data for
    """
    from fintrack_be.functions.stock.stock_data import get_stock_data, bulk_stock_price_data_to_model
    from fintrack_be.models import Exchange, Stock

    exchange = Exchange.objects.get(symbol=exchange_symbol)
    stocks = Stock.objects.filter(exchange=exchange).order_by('symbol')

    for stock in stocks:
        df = get_stock_data(symbol=stock.symbol, period='max', interval='1m')
        bulk_stock_price_data_to_model(df)
        print('Added {} daily minute data'.format(stock.symbol))
