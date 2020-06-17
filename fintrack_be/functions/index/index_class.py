from django.db import IntegrityError

from fintrack_be.models import Index


class IndexClass:
    """
    Index Parent class that is the blueprint for indices in the system
    """
    def __init__(self, name, symbol, constituent_links):
        self.name = name
        self.symbol = symbol
        self.constituent_links = constituent_links

    def create_index(self):
        try:
            Index.objects.create(symbol=self.symbol,
                                 name=self.name)
        except IntegrityError:
            print('Index Instance already exists')
