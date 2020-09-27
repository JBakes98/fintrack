import pandas as pd
from django.db import models
from index.managers import IndexManager
from stock.models import Stock


class Index(models.Model):
    symbol = models.CharField(max_length=25, unique=True, null=False, blank=False)
    name = models.CharField(max_length=125)
    constituents = models.ManyToManyField(Stock, through='IndexConstituents', blank=True)
    correlation = models.JSONField(default=None, blank=True, null=True)

    objects = IndexManager()

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = 'Indices'
        ordering = ['symbol', ]

    def __str__(self):
        return self.symbol

    @property
    def constituents_count(self):
        return self.constituents.count()

    def put_correlation(self, dataframe):
        self.correlation = dataframe.to_json()
        self.save()

    def load_correlation(self):
        return pd.read_json(self.correlation)
