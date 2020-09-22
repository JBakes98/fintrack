import os

import pandas as pd
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q

from index.models import Index


class IndexService:
    def __init__(self, name=None, symbol=None):
        self._name = name
        self._symbol = symbol

    def _get_index_obj(self):
        try:
            index = Index.objects.get(Q(symbol=self._symbol) | Q(name=self._name))
            self._name = index.name
            self._symbol = index.symbol
            return index
        except Index.DoesNotExist as e:
            raise e

    def create_index(self):
        try:
            Index.objects.create_index(symbol=self._symbol, name=self._name)
        except IntegrityError as e:
            raise e

    def get_index_constituent_correlation(self):
        index = self._get_index_obj()
        if not os.path.exists('{}-joined-closes.csv'.format(index.name)):
            self.compile_index_constituents_data()

        df = pd.read_csv('{}{}-joined-closes.csv'.format(settings.MEDIA_ROOT, index.symbol))
        df_corr = df.corr()

        return df_corr

    def compile_index_constituents_data(self):
        # Selects all of the stock constituents for the index
        index = self._get_index_obj()
        stocks = index.constituents.all()
        main_df = pd.DataFrame()

        # Iterates through the stocks and gets their relevant price information and puts it into
        # a combined df, main_df
        for stock in stocks:
            df = stock.get_price_data()

            # Check that the stock has any price data available
            if not df.empty:
                # Format the df to have the timestamp column as the index and then name the close column
                # the stocks symbol so it can be identified and then drop the data thats not needed
                df.set_index('timestamp', inplace=True)
                df.rename(columns={'close': stock.ticker}, inplace=True)
                df.drop(
                    ['id', 'stock_id', 'open', 'high', 'low', 'volume', 'change', 'change_perc', 'ml_prediction'],
                    1,
                    inplace=True)

                # If main df is empty set it to the df otherwise add it to the
                # existing main df
                if main_df.empty:
                    main_df = df
                else:
                    main_df = main_df.join(df, how='outer')

        main_df.to_csv('{}{}-joined-closes.csv'.format(settings.MEDIA_ROOT, index.symbol),
                       encoding='utf-8', index=False)
