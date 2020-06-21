import pandas as pd
from index.models import IndexConstituents, Index
from stock.models import Stock


class StockMachineLearningService:
    @staticmethod
    def process_data_for_labels(ticker):
        hm_days = 7

        # Get the index that the stock has been part of the longest and get the joint
        # csv file for that index
        stock = Stock.objects.get(ticker=ticker)
        stock_index = IndexConstituents.objects.filter(constituent=stock).order_by('date_joined')[0]
        index = Index.objects.get(id=stock_index.index_id)
        df = pd.read_csv('index/csv/{}-joined-closes.csv'.format(index.name), index_col=0)

        tickers = df.columns.values.tolist()
        df.fillna(0, inplace=True)

        for i in range(1, hm_days + 1):
            df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        df.fillna(0, inplace=True)

        return tickers, df
