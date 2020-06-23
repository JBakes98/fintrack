import decimal
import pandas as pd
from django.db import IntegrityError
from fintrack_be.models import Stock, StockPriceData


def stock_price_data_df_to_model(df):
    """
    Method that iterates of a stock price dataframe and creates its relevent models,
    this doesnt use bulk create and inserts data until it hits an already existing
    entry.
    :param df: Stock price dataframe
    """
    for row in df[::-1].itertuples():
        try:
            print(row)
            StockPriceData.objects.create(timestamp=getattr(row, 'Index'),
                                          open=getattr(row, 'open'),
                                          high=getattr(row, 'high'),
                                          low=getattr(row, 'low'),
                                          close=getattr(row, 'close'),
                                          volume=getattr(row, 'volume'),
                                          stock=getattr(row, 'stock'),
                                          change=getattr(row, 'change'),
                                          change_perc=getattr(row, 'change_perc'))
        except IntegrityError as e:
            print('{}'.format(e))
            break
        except decimal.InvalidOperation as e:
            print(e)


def bulk_stock_price_data_to_model(df):
    """
    Same method as stock_price_data_df_to_model however iterates
    through the df but uses the bulk_create method to increase
    insert efficiency.
    :param df: Dataframe containing stock price data
    """
    try:
        data = [StockPriceData(timestamp=getattr(row, 'Index'),
                               open=getattr(row, 'open'),
                               high=getattr(row, 'high'),
                               low=getattr(row, 'low'),
                               close=getattr(row, 'close'),
                               volume=getattr(row, 'volume'),
                               stock=getattr(row, 'stock'),
                               change=getattr(row, 'change'),
                               change_perc=getattr(row, 'change_perc')
                               )
                for row in df.itertuples()]
        StockPriceData.objects.bulk_create(data)

    except IntegrityError as e:
        print('Already contain data for this stock {}'.format(e))
    except decimal.InvalidOperation as e:
        print(e)


def prepare_stock_data_df(df, ticker):
    """
    Method that runs necessary methods to prepare a df
    for use in one method, saves calling individual methods
    """
    df = format_stock_data(df, ticker)
    df = add_change_data(df)

    return df


def format_stock_data(df, ticker):
    """
    Takes stock data df and formats it to model fields for easy interaction throughout the program,
    also adds the stock to the df so that the df can find the parent of the data.
    :param df: Stock price data in a dataframe
    :param ticker: The Stocks ticker
    :return: The formatted dataframe
    """
    try:
        stock = Stock.objects.get(ticker=ticker)
    except Stock.DoesNotExist as e:
        print(e)
        return

    formatted_df = df.rename(
        columns={'Open': 'open',
                 'High': 'high',
                 'Low': 'low',
                 'Close': 'close',
                 'Volume': 'volume',
                 })

    formatted_df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True, errors='ignore')
    formatted_df.rename_axis('timestamp', axis='index', inplace=True)
    formatted_df['stock'] = stock
    formatted_df.fillna(0.00, inplace=True)

    return formatted_df


def add_change_data(df):
    """
    Method that takes a stocks data df and adds the change columns to df,
    df must be formatted before being passed into this method
    :param df: A dataframe containing stock price data
    :return: The stock price dataframe with the added change columns
    """
    pd.set_option('use_inf_as_na', True)
    df['change'] = df.close.diff()
    df['change_perc'] = df.close.pct_change() * 100

    df['change'] = df.change.fillna(0).astype(float)
    df['change_perc'] = df.change_perc.fillna(0).astype(float)

    return df
