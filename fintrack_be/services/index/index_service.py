import pandas as pd
import os
from fintrack_be.models import Index


class IndexService:
    @staticmethod
    def compile_index_constituents_data(index):
        # Selects all of the stock constituents for the index
        try:
            index = Index.objects.get(symbol=index)
        except Index.DoesNotExist as e:
            raise e

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

        main_df.to_csv('{}-joined-closes.csv'.format(index.name))

    def get_index_constituent_correlation(self, index):
        try:
            index = Index.objects.get(symbol=index)
        except Index.DoesNotExist as e:
            raise e

        if not os.path.exists('{}-joined-closes.csv'.format(index.name)):
            self.compile_index_constituents_data(index.symbol)

        df = pd.read_csv('{}-joined-closes.csv'.format(index.name))
        df_corr = df.corr()

        return df_corr
