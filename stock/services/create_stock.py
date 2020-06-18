import pandas as pd
from django.db import IntegrityError
from django.db.models import Q
from exchange.models import Exchange
from company.models import Company
from stock.models import Stock
from stock.services import get_stock_company


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