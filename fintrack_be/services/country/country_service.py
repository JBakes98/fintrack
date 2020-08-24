import requests
import bs4 as bs
from fintrack_be.models import Country


class CountryDataService:
    def __init__(self, name, alpha2, alpha3, numeric):
        self.name = name
        self.alpha2 = alpha2
        self.alpha3 = alpha3
        self.numeric = numeric
