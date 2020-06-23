from django.db import models
import pandas as pd
from fintrack_be.models.stock import Stock
import os


class Index(models.Model):
    symbol = models.CharField(max_length=25, unique=True, null=False, blank=False)
    name = models.CharField(max_length=125)
    constituents = models.ManyToManyField(Stock, through='IndexConstituents', blank=True)

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Indices'
        ordering = ['symbol', ]

    def __str__(self):
        return self.symbol

    def constituents_count(self):
        return self.constituents.count()

    def compile_index_constituents_data(self):
        # Selects all of the stock constituents for the index
        stocks = self.constituents.all()
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

        main_df.to_csv('index/csv/{}-joined-closes.csv'.format(self.name))

    def get_index_constituent_correlation(self):
        if not os.path.exists('index/csv/{}-joined-closes.csv'.format(self.name)):
            self.compile_index_constituents_data()

        df = pd.read_csv('index/csv/{}-joined-closes.csv'.format(self.name))
        df_corr = df.corr()
        return df_corr
