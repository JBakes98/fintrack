from dataclasses import dataclass
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
from stock.utils import DFUtil


@dataclass
class StockDto:
    ticker: str
    name: str
    exchange: str
    company: str


class StockDataService:
    def create_stock(self, ticker, name, exchange):
        """
        Method for creating a stock and finding its parent company object
        :param ticker: Stocks ticker
        :param name: Stocks name
        :param exchange: Stocks parent Exchange
        """
        try:
            exchange = Exchange.objects.get(Q(symbol=exchange) | Q(name=exchange))
            company = self.get_stock_company(ticker)
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

    @staticmethod
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
                short_company_name, long_company_name = company_json_util.extract_company_names_from_json(json)
                try:
                    return Company.objects.get(Q(short_name=short_company_name) | Q(long_name=long_company_name))
                except Company.DoesNotExist:
                    Company.objects.create_company_json(json)
                    return Company.objects.get(Q(short_name=short_company_name) | Q(long_name=long_company_name))

            except ValueError:
                print('{} cannot find parent company'.format(ticker))
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

    @staticmethod
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

        return DFUtil.prepare_stock_data_df(df, ticker)
