from django.db import IntegrityError

from fintrack_be.models import Country
from fintrack_be.models import Exchange


class ExchangeClass:
    """
    Exchange Parent class that is the blueprint for the Exchanges used in the system
    """
    def __init__(self, name, symbol, stock_links, country, timezone, opening_time, closing_time):
        self.name = name
        self.symbol = symbol
        self.stock_links = stock_links
        self.country = country
        self.timezone = timezone
        self.opening_time = opening_time
        self.closing_time = closing_time

    def create_exchange(self):
        try:
            country_object = Country.objects.get(alpha2=self.country)
            Exchange.objects.create(symbol=self.symbol,
                                    name=self.name,
                                    country=country_object,
                                    timezone=self.timezone,
                                    opening_time=self.opening_time,
                                    closing_time=self.closing_time)
        except IntegrityError:
            print('Exchange Instance already exists')
