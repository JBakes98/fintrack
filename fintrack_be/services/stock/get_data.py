from http.client import IncompleteRead
import yfinance as yf
from django.core.exceptions import MultipleObjectsReturned

from fintrack_be.models import Company
from fintrack_be.services.company.company_data import get_company, extract_company_names_from_json, create_company_json
from fintrack_be.services.stock.df_services import prepare_stock_data_df


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
            short_company_name, long_company_name = extract_company_names_from_json(json)

            try:
                return get_company(short_company_name, long_company_name)
            except Company.DoesNotExist:
                create_company_json(json)
                return get_company(short_company_name, long_company_name)

        except ValueError:
            print('{} cannot find parent company'.format(ticker))
            return get_company('N/A', 'Non linked objects')
        except KeyError:
            return get_company('N/A', 'Non linked objects')
        except IncompleteRead as e:
            print(e)
        except MultipleObjectsReturned as e:
            print(e)
        # except HTTPError as e:
        #     if i < attempts - 1:
        #         print(e)
        #         print('Retrying attempt {}'.format(i))
        #         continue
        #     else:
        #         print(e)
        #         print('Attempted {} times, all unsuccessful'.format(attempts))
        #     break


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

    return prepare_stock_data_df(df, ticker)