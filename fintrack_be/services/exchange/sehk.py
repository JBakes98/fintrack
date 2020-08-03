from fintrack_be.services.exchange.exchange_class import ExchangeClass
from fintrack_be.services.stock.stock_data import StockDataService
import requests
import bs4 as bs
import datetime


class SEHK(ExchangeClass):
    """
    ExchangeClass child
    """
    def __init__(self):
        self.name = 'Hong Kong Stock Exchange'
        self.symbol = 'SEHK'
        self.stock_links = ('https://eoddata.com/stocklist/HKEX.htm', '')
        self.country = 'HK'
        self.timezone = 'HKT'
        self.opening_time = datetime.time(hour=9, minute=30)
        self.closing_time = datetime.time(hour=16)

    def create_stocks(self):
        """ Function for creating classes stocks """
        for link in self.stock_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, "lxml")
            table = soup.find('table', {'class': 'quotes'})

            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[0].text
                ticker = ticker[1:]
                mapping = str.maketrans(".", "-")
                ticker = ticker.translate(mapping) + ".HK"
                name = row.findAll('td')[1].text
                StockDataService.create_stock(ticker, name, self.symbol)
