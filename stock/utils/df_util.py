import pandas as pd

from stock.models import Stock


class DFUtil:
    @staticmethod
    def prepare_stock_data_df(self, df, ticker):
        """
        Method that runs necessary methods to prepare a df
        for use in one method, saves calling individual methods
        """
        df = self.format_stock_data(df, ticker)
        df = self.add_change_data(df)

        return df

    @staticmethod
    def format_stock_data(df, ticker):
        """
        Takes stock data df and formats it to model fields for easy interaction throughout the program,
        also adds the stock to the df so that the df can find the parent of the data.
        :param df: Stock price data in a dataframe
        :param ticker: The Stocks ticker
        :return: The formatted dataframe
        """
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist as e:
            print(e)
            return

        formatted_df = df.rename(
            columns={'Open': 'open',
                     'High': 'high',
                     'Low': 'low',
                     'Close': 'close',
                     'Volume': 'volume',
                     })

        formatted_df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True, errors='ignore')
        formatted_df.rename_axis('timestamp', axis='index', inplace=True)
        formatted_df['stock'] = stock
        formatted_df.fillna(0.00, inplace=True)

        return formatted_df

    @staticmethod
    def add_change_data(df):
        """
        Method that takes a stocks data df and adds the change columns to df,
        df must be formatted before being passed into this method
        :param df: A dataframe containing stock price data
        :return: The stock price dataframe with the added change columns
        """
        pd.set_option('use_inf_as_na', True)
        df['change'] = df.close.diff()
        df['change_perc'] = df.close.pct_change() * 100

        df['change'] = df.change.fillna(0).astype(float)
        df['change_perc'] = df.change_perc.fillna(0).astype(float)

        return df
