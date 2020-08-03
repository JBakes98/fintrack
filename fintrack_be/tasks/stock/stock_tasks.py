from __future__ import absolute_import, unicode_literals
from celery import task


@task()
def get_latest_stock_data(ticker):
    """
    Method that gets the latest data for a Stock
    :param ticker: Ticker of Stock to get data for
    """
    from fintrack_be.models import StockPriceData
    from fintrack_be.services.stock.stock_data import StockDataService

    df = StockDataService.get_stock_data(ticker, period='1d', interval='1m')
    StockPriceData.objects.create_df_data(df)
    print('Added {} minute data'.format(ticker))


@task
def get_day_stock_data(ticker):
    """
    Method that that gets the day data for a Stock
    :param ticker: Stock ticker to get data for
    """
    from fintrack_be.models import StockPriceData
    from fintrack_be.services.stock.stock_data import StockDataService

    df = StockDataService.get_stock_data(ticker, period='1d', interval='1d')
    StockPriceData.objects.create_df_data(df)
    print('Added {} day data'.format(ticker))


@task
def get_bulk_day_stock_data(ticker):
    """
    Method that that gets the day data for a Stock
    :param ticker: Stock symbool to get data for
    """
    from fintrack_be.models import StockPriceData
    from fintrack_be.services.stock.stock_data import StockDataService

    df = StockDataService.get_stock_data(ticker, period='1y', interval='1d')
    StockPriceData.objects.create_bulk_data(df)
    print('Added {} daily data'.format(ticker))
