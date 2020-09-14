from django.contrib.auth import get_user_model
from django.db import models
import pandas as pd
from django.urls import reverse

from stock.helpers import timezone_helper as tz_help
from exchange.models import Exchange
from company.models import Company

UserModel = get_user_model()


class Stock(models.Model):
    ticker = models.CharField(unique=True, max_length=15, null=False, blank=False)
    name = models.CharField(max_length=255)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='exchange_stocks')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, related_name='company_stocks')
    watchlist = models.ManyToManyField(UserModel, related_name='stock_watchlist')

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ['exchange', 'company', 'ticker']

    def __str__(self):
        return self.ticker

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ticker', 'name', 'exchange_id'], name='exchange_stock')
        ]

    def get_absolute_url(self):
        return reverse('fintrack_be:stock-detail', kwargs={'ticker': self.ticker})

    @property
    def market_local_timestamp(self):
        timezone = tz_help.get_timezone(self.exchange.timezone, self.exchange.country.alpha2)
        local_timestamp = tz_help.convert_datetime_to_timezone(self.stock_data.order_by('-timestamp').timestamp, "UTC",
                                                       timezone)
        return local_timestamp

    @property
    def latest_price(self):
        data = self.stock_prices.first()
        return data.close

    @property
    def latest_data(self):
        return self.stock_prices.first()

    def get_price_data(self):
        return pd.DataFrame(list(self.stock_prices.all().values()))
