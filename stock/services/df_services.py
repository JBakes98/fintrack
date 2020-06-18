import decimal
from django.db import IntegrityError
from stock.models import StockPriceData


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
