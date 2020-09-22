from exchange.services import ExchangeClass
from stock.services import StockDataService
import requests
import bs4 as bs
import datetime


class NASDAQ(ExchangeClass):
    """
    ExchangeClass child
    """
    def __init__(self):
        self._name = 'Nasdaq'
        self._symbol = 'NASDAQ'
        self._stock_links = ('http://eoddata.com/stocklist/NASDAQ/A.htm',
                            'http://eoddata.com/stocklist/NASDAQ/B.htm',
                            'http://eoddata.com/stocklist/NASDAQ/C.htm',
                            'http://eoddata.com/stocklist/NASDAQ/D.htm',
                            'http://eoddata.com/stocklist/NASDAQ/E.htm',
                            'http://eoddata.com/stocklist/NASDAQ/F.htm',
                            'http://eoddata.com/stocklist/NASDAQ/G.htm',
                            'http://eoddata.com/stocklist/NASDAQ/H.htm',
                            'http://eoddata.com/stocklist/NASDAQ/I.htm',
                            'http://eoddata.com/stocklist/NASDAQ/J.htm',
                            'http://eoddata.com/stocklist/NASDAQ/K.htm',
                            'http://eoddata.com/stocklist/NASDAQ/L.htm',
                            'http://eoddata.com/stocklist/NASDAQ/M.htm',
                            'http://eoddata.com/stocklist/NASDAQ/N.htm',
                            'http://eoddata.com/stocklist/NASDAQ/O.htm',
                            'http://eoddata.com/stocklist/NASDAQ/P.htm',
                            'http://eoddata.com/stocklist/NASDAQ/Q.htm',
                            'http://eoddata.com/stocklist/NASDAQ/R.htm',
                            'http://eoddata.com/stocklist/NASDAQ/S.htm',
                            'http://eoddata.com/stocklist/NASDAQ/T.htm',
                            'http://eoddata.com/stocklist/NASDAQ/U.htm',
                            'http://eoddata.com/stocklist/NASDAQ/V.htm',
                            'http://eoddata.com/stocklist/NASDAQ/W.htm',
                            'http://eoddata.com/stocklist/NASDAQ/X.htm',
                            'http://eoddata.com/stocklist/NASDAQ/Y.htm',
                            'http://eoddata.com/stocklist/NASDAQ/Z.htm',)
        self._country = 'US'
        self._timezone = 'EST'
        self._opening_time = datetime.time(hour=9, minute=30)
        self._closing_time = datetime.time(hour=16)

    def create_stocks(self):
        """ Function for creating classes stocks """
        for link in self._stock_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, "lxml")
            table = soup.find('table', {'class': 'quotes'})

            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[0].text
                mapping = str.maketrans(".", "-")
                ticker = ticker.translate(mapping)
                name = row.findAll('td')[1].text
                StockDataService(ticker=ticker, name=name, exchange=self._symbol).create_stock()
