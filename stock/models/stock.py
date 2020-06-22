from django.db import models
import pandas as pd

from fintrack.helper.timezone_helper import get_timezone, convert_datetime_to_timezone
from exchange.models import Exchange
from company.models import Company


class Stock(models.Model):
    ticker = models.CharField(unique=True, max_length=15, null=False, blank=False)
    name = models.CharField(max_length=255)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='exchange_stocks')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, related_name='company_stocks')

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ('ticker', )
        db_table = 'stock'

    def __str__(self):
        return self.ticker

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ticker', 'name', 'exchange_id'], name='exchange_stock')
        ]

    @property
    def market_local_timestamp(self):
        timezone = get_timezone(self.exchange.timezone, self.exchange.country.alpha2)
        local_timestamp = convert_datetime_to_timezone(self.stock_data.order_by('-timestamp').timestamp, "UTC",
                                                       timezone)
        return local_timestamp

    @property
    def latest_price(self):
        data = self.stock_prices.first()
        return data.close

    def get_price_data(self):
        return pd.DataFrame(list(self.stock_data.all().values()))
