import pandas as pd
from stock.services import StockDataService


class StockMachineLearningService:
    def __init__(self, stocks: []):
        self._stocks = stocks
        self._stocks_closes = None

    def compile_stocks_close_data(self):
        """
        Compiles the closing price data of the stocks and returns a
        dataframe with dates and the stocks respective closing price
        on that date.
        :return: Dataframe of stock closing prices on dates
        """
        main_df = pd.DataFrame()

        # Iterates through the stocks and gets their relevant price information and puts it into
        # a combined df, main_df
        for stock in self._stocks:
            df = StockDataService(ticker=stock).get_price_data()

            # Check that the stock has any price data available
            if not df.empty:
                # Format the df to have the timestamp column as the index and then name the close column
                # the stocks symbol so it can be identified and then drop the data that's not needed
                df.set_index('timestamp', inplace=True)
                df.rename(columns={'close': stock}, inplace=True)
                df.drop(['id', 'stock_id', 'open', 'high', 'low', 'volume', 'change', 'change_perc', 'ml_prediction'],
                        1, inplace=True)

                # Set the column to the float dtype instead of object, this is needed unlike
                # index example as thats read from csv into float dtype automatically
                df[stock] = df[stock].astype(float)

                # If main df is empty set it to the df otherwise add it to the
                # existing main df
                if main_df.empty:
                    main_df = df
                else:
                    main_df = main_df.join(df, how='outer')

        main_df.reset_index(drop=True, inplace=True)
        return main_df

    def get_stocks_correlation(self):
        """
        Reads the stocks closing data into a dataframe,
        if this file is empty it will run the function to
        compile the close data. A dataframe based off the
        built in pandas dataframe function .corr() which
        calculates the correlation of the stocks.
        :return: Dataframe of stocks correlations
        """
        if self._stocks_closes is None:
            self.compile_stocks_close_data()

        df = self.compile_stocks_close_data()
        return df.corr()
