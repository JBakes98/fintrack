import pandas as pd
from django.db import IntegrityError
from django.db.models import Q
from fintrack_be.models import Exchange
from fintrack_be.models import Company
from fintrack_be.models import Stock
from fintrack_be.services.stock.get_data import get_stock_company


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


def run_ml_processing(index):
    main_df = pd.DataFrame()

    stocks = Stock.objects.filter()