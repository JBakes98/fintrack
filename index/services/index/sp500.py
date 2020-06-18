from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from index.services.index.index_class import IndexClass
from index.models import Index, IndexConstituents
from stock.models import Stock

import requests
import bs4 as bs


class SP500(IndexClass):
    """
    IndexClass Child
    """

    def __init__(self):
        self.name = 'S&P 500'
        self.symbol = '^GSPC'
        self.constituent_links = ('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',)

    def add_constituents(self):
        """
        Method for adding the indices constituents
        """
        for link in self.constituent_links:
            resp = requests.get(link)
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'id': 'constituents'})

            for row in table.findAll('tr')[1:]:
                stock = row.findAll('td')[0].text[:-1]
                added = row.findAll('td')[6].text[:10]

                mapping = str.maketrans(".", "-")
                stock = stock.translate(mapping)

                print(stock)
                print(added)

                try:
                    stock = Stock.objects.get(ticker=stock)
                    index = Index.objects.get(symbol=self.symbol)

                    if added:
                        IndexConstituents.objects.create(constituent=stock,
                                                         index=index,
                                                         date_joined=added)
                    else:
                        IndexConstituents.objects.create(constituent=stock,
                                                         index=index)

                    print('{} added as a constituent of {}'.format(stock.ticker, self.name))

                except ObjectDoesNotExist as e:
                    print(e)

                except IntegrityError as e:
                    print(e)
