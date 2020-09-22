from django.db import IntegrityError

from country.models import Country
from exchange.models import Exchange


class ExchangeClass:
    """
    Exchange Parent class that is the blueprint for the Exchanges used in the system
    """
    def __init__(self, name, symbol, stock_links, country, timezone, opening_time, closing_time):
        self._name = name
        self._symbol = symbol
        self._stock_links = stock_links
        self._country = country
        self._timezone = timezone
        self._opening_time = opening_time
        self._closing_time = closing_time

    def create_exchange(self):
        try:
            country_obj = Country.objects.get(alpha2=self._country)
            Exchange.objects.create_exchange(symbol=self._symbol,
                                             name=self._name,
                                             country=country_obj,
                                             timezone=self._timezone,
                                             opening_time=self._opening_time,
                                             closing_time=self._closing_time)
        except IntegrityError:
            print('Exchange Instance already exists')

    def create_stocks(self):
        pass
