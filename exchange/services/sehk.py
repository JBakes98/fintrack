from exchange.services import ExchangeClass
from stock.services import StockDataService
import requests
import bs4 as bs
import datetime


class SEHK(ExchangeClass):
    """
    ExchangeClass child
    """
    def __init__(self):
        self._name = 'Hong Kong Stock Exchange'
        self._symbol = 'SEHK'
        self._stock_links = ('https://eoddata.com/stocklist/HKEX.htm', '')
        self._country = 'HK'
        self._timezone = 'HKT'
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
                ticker = ticker[1:]
                mapping = str.maketrans(".", "-")
                ticker = ticker.translate(mapping) + ".HK"
                name = row.findAll('td')[1].text
                StockDataService(ticker=ticker, name=name, exchange=self._symbol).create_stock()
