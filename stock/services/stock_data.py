from http.client import IncompleteRead
from urllib.error import HTTPError
from django.db import IntegrityError
from django.db.models import Q
import yfinance as yf
from django.core.exceptions import MultipleObjectsReturned
from company.models import Company
from exchange.models import Exchange
from stock.models import Stock
from company.utils import company_json_util
from stock.utils import df_util


class StockDataService:
    def __init__(self, ticker, name, exchange):
        self._ticker = ticker
        self._name = name
        self._exchange = exchange

    def create_stock(self):
        """
        Method for creating a stock and finding its parent company object
        :param ticker: Stocks ticker
        :param name: Stocks name
        :param exchange: Stocks parent Exchange
        """
        try:
            exchange_obj = Exchange.objects.get(Q(symbol=self._exchange) | Q(name=self._exchange))
            company_obj = self.get_stock_company()
            Stock.objects.update_or_create(ticker=self._ticker,
                                           name=self._name,
                                           exchange=exchange_obj,
                                           company=company_obj)
            print('{} created'.format(self._ticker))

        except Exchange.DoesNotExist as e:
            print('{}: {}'.format(self._exchange, e))
        except Company.DoesNotExist as e:
            print('{}'.format(e))
        except KeyError as e:
            print('{}'.format(e))
        except IntegrityError as e:
            print(e)

    def get_stock_company(self):
        """
        Method for getting the parent company of the specified stock, if company cannot be found
        then it will call the create_company method to create the company. If the method fails
        it will attempt 3 times before failing completely.
        :param ticker: Stock ticker
        :return: Stocks parent Company
        """
        # Returns JSON data that contains data on the stock
        stock = yf.Ticker(self._ticker)
        attempts = 3

        for i in range(attempts):
            try:
                json = stock.info
                # Get company names from the JSON response data
                short_company_name, long_company_name = company_json_util.extract_company_names_from_json(json)
                try:
                    return Company.objects.get(Q(short_name=short_company_name) | Q(long_name=long_company_name))
                except Company.DoesNotExist:
                    Company.objects.create_company_json(json)
                    return Company.objects.get(Q(short_name=short_company_name) | Q(long_name=long_company_name))

            except ValueError:
                print('{} cannot find parent company'.format(self._ticker))
                return Company.objects.get(Q(short_name='N/A') | Q(long_name='Non linked objects'))
            except KeyError:
                return Company.objects.get(Q(short_name='N/A') | Q(long_name='Non linked objects'))
            except IncompleteRead as e:
                print(e)
            except MultipleObjectsReturned as e:
                print(e)
            except HTTPError as e:
                if i < attempts - 1:
                    print(e)
                    print('Retrying attempt {}'.format(i))
                    continue
                else:
                    print(e)
                    print('Attempted {} times, all unsuccessful'.format(attempts))
                break

    def get_stock_data(self, period='10Y', interval='1d'):
        """
        This method gets a specific stocks price data in a 1 day interval and puts
        it into a dataframe
        :param interval: Interval of data that should be retrieved, options are 1m, 1d, 1m, 1y
        :param period: Period of data that should be retrieved
        :param ticker: Stocks ticker
        :return: Stocks price data dataframe
        """
        stock = yf.Ticker(self._ticker)
        df = stock.history(period=period, interval=interval)

        return df_util.prepare_stock_data_df(df, self._ticker)
