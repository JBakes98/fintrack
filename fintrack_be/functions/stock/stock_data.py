import decimal
import pandas as pd

from urllib.error import HTTPError
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned

import yfinance as yf
from http.client import IncompleteRead

from fintrack_be.models import Exchange, Stock, StockPriceData, Company
from fintrack_be.functions.company import company_data
from fintrack_be.helpers import dataframe_helper as df_helper


def create_stock(ticker, name, exchange):
    """
    Method for creating a stock and finding its parent company object
    :param ticker: Stocks ticker
    :param name: Stocks name
    :param exchange: Stocks parent Exchange
    """
    try:
        exchange = Exchange.objects.get(Q(symbol=exchange) | Q(name=exchange))
        company = get_stock_company(ticker)
        Stock.objects.update_or_create(ticker=ticker,
                                       name=name,
                                       exchange=exchange,
                                       company=company)
        print('{} created'.format(ticker))

    except Exchange.DoesNotExist as e:
        print('{}: {}'.format(exchange, e))
    except Company.DoesNotExist as e:
        print('{}'.format(e))
    except KeyError as e:
        print('{}'.format(e))
    except IntegrityError as e:
        print(e)


def get_stock_company(ticker):
    """
    Method for getting the parent company of the specified stock, if company cannot be found
    then it will call the create_company method to create the company. If the method fails
    it will attempt 3 times before failing completely.
    :param ticker: Stock ticker
    :return: Stocks parent Company
    """
    # Returns JSON data that contains data on the stock
    stock = yf.Ticker(ticker)
    attempts = 3

    for i in range(attempts):
        try:
            json = stock.info
            # Get company names from the JSON response data
            short_company_name, long_company_name = company_data.extract_company_names_from_json(json)

            try:
                return company_data.get_company(short_company_name, long_company_name)
            except Company.DoesNotExist:
                company_data.create_company_json(json)
                return company_data.get_company(short_company_name, long_company_name)

        except ValueError:
            print('{} cannot find parent company'.format(ticker))
            return company_data.get_company('N/A', 'Non linked objects')
        except KeyError:
            return company_data.get_company('N/A', 'Non linked objects')
        except IncompleteRead as e:
            print(e)
        except MultipleObjectsReturned as e:
            print(e)
        except HTTPError as e:
            print(e)
            if i < attempts - 1:
                print('Retrying attempt {}'.format(i))
                continue
            else:
                print(e)
                print('Attempted {} times, all unsuccessful'.format(attempts))
            break


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


def get_stock_data(ticker, period, interval):
    """
    This method gets a specific stocks price data in a 1 day interval and puts
    it into a dataframe
    :param interval: Interval of data that should be retrieved, options are 1m, 1d, 1m, 1y
    :param period: Period of data that should be retrieved
    :param ticker: Stocks ticker
    :return: Stocks price data dataframe
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)

    return df_helper.prepare_stock_data_df(df, ticker)


def run_ml_processing(index):
    main_df = pd.DataFrame()

    stocks = Stock.objects.filter()