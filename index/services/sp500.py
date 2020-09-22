import requests
import bs4 as bs
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from index.models import Index, IndexConstituents
from stock.models import Stock
from index.services import IndexService


class SP500(IndexService):
    """
    Specific service class for Index which will contain the functions to create the
    index, once created the IndexService should be used.
    """
    def __init__(self):
        self._name = 'S&P 500'
        self._symbol = '^GSPC'
        self._constituent_links = ('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',)

    def add_constituents(self):
        """
        Method for adding the indices constituents
        """
        for link in self._constituent_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'id': 'constituents'})

            for row in table.findAll('tr')[1:]:
                stock = row.findAll('td')[0].text[:-1]
                added = row.findAll('td')[6].text[:10]
                mapping = str.maketrans(".", "-")
                stock = stock.translate(mapping)

                try:
                    stock = Stock.objects.get(ticker=stock)
                    index = Index.objects.get(symbol=self._symbol)
                    if added:
                        IndexConstituents.objects.create(constituent=stock, index=index, date_joined=added)
                    else:
                        IndexConstituents.objects.create(constituent=stock, index=index)
                    print('{} added as a constituent of {}'.format(stock.ticker, self._name))

                except ObjectDoesNotExist as e:
                    print(e)
                except IntegrityError as e:
                    print(e)