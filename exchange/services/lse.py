from exchange.services.exchange_class import ExchangeClass
from stock.services.create_stock import create_stock
import requests
import bs4 as bs
import datetime


class LSE(ExchangeClass):
    """
    ExchangeClass child
    """
    def __init__(self):
        self.name = 'London Stock Exchange'
        self.symbol = 'LSE'
        self.stock_links = ('http://eoddata.com/stocklist/LSE/0.htm',
                            'http://eoddata.com/stocklist/LSE/3.htm',
                            'http://eoddata.com/stocklist/LSE/4.htm',
                            'http://eoddata.com/stocklist/LSE/5.htm',
                            'http://eoddata.com/stocklist/LSE/6.htm',
                            'http://eoddata.com/stocklist/LSE/7.htm',
                            'http://eoddata.com/stocklist/LSE/8.htm',
                            'http://eoddata.com/stocklist/LSE/9.htm',
                            'http://eoddata.com/stocklist/LSE/A.htm',
                            'http://eoddata.com/stocklist/LSE/B.htm',
                            'http://eoddata.com/stocklist/LSE/C.htm',
                            'http://eoddata.com/stocklist/LSE/D.htm',
                            'http://eoddata.com/stocklist/LSE/E.htm',
                            'http://eoddata.com/stocklist/LSE/F.htm',
                            'http://eoddata.com/stocklist/LSE/G.htm',
                            'http://eoddata.com/stocklist/LSE/H.htm',
                            'http://eoddata.com/stocklist/LSE/I.htm',
                            'http://eoddata.com/stocklist/LSE/J.htm',
                            'http://eoddata.com/stocklist/LSE/K.htm',
                            'http://eoddata.com/stocklist/LSE/L.htm',
                            'http://eoddata.com/stocklist/LSE/M.htm',
                            'http://eoddata.com/stocklist/LSE/N.htm',
                            'http://eoddata.com/stocklist/LSE/O.htm',
                            'http://eoddata.com/stocklist/LSE/P.htm',
                            'http://eoddata.com/stocklist/LSE/Q.htm',
                            'http://eoddata.com/stocklist/LSE/R.htm',
                            'http://eoddata.com/stocklist/LSE/S.htm',
                            'http://eoddata.com/stocklist/LSE/T.htm',
                            'http://eoddata.com/stocklist/LSE/U.htm',
                            'http://eoddata.com/stocklist/LSE/V.htm',
                            'http://eoddata.com/stocklist/LSE/W.htm',
                            'http://eoddata.com/stocklist/LSE/X.htm',
                            'http://eoddata.com/stocklist/LSE/Y.htm',
                            'http://eoddata.com/stocklist/LSE/Z.htm',)
        self.country = 'GB'
        self.timezone = 'BST'
        self.opening_time = datetime.time(hour=8)
        self.closing_time = datetime.time(hour=16, minute=30)

    def create_stocks(self):
        """ Method for creating all of the classes listed stocks """
        for link in self.stock_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, "lxml")
            table = soup.find('table', {'class': 'quotes'})

            for row in table.findAll('tr')[1:]:
                ticker = row.findAll('td')[0].text
                mapping = str.maketrans(".", "-")

                ticker = ticker.translate(mapping) + ".L"
                name = row.findAll('td')[1].text

                create_stock(ticker, name, self.symbol)
