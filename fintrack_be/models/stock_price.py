from decimal import Decimal

from django.db import models
from django.urls import reverse

from fintrack_be.models.stock import Stock
from fintrack_be.managers.stock_price_manager import StockPriceManager
from fintrack_be.helpers import timezone_helper
from fintrack_be.choice_options import PREDICTION_OPTIONS


class StockPriceData(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    stock = models.ForeignKey(Stock, related_name='stock_prices', on_delete=models.CASCADE)

    high = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    low = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    open = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    close = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    volume = models.BigIntegerField(blank=True, null=True)

    change = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    change_perc = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))

    ml_prediction = models.CharField(max_length=4, choices=PREDICTION_OPTIONS, default=PREDICTION_OPTIONS[2])

    objects = StockPriceManager()

    class Meta:
        verbose_name = 'Stock Price Data'
        verbose_name_plural = 'Stocks Price Data'
        ordering = ['stock', '-timestamp']

        indexes = [
            models.Index(fields=['timestamp', 'stock']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['stock', 'timestamp'], name='unique_stock_data')
        ]

    def __str__(self):
        string = self.stock.symbol + ' ' + str(self.timestamp)
        return string

    def get_absolute_url(self):
        return reverse('fintrack_be:price', kwargs={'pk': self.pk})

    @property
    def timestamp_in_market_time(self):
        """
        Method that returns the price data timestamp in the market local time from the
        stored UTC time
        :return: Timestamp in local timezone
        """
        timezone = timezone_helper.get_timezone(self.stock.exchange.timezone, self.stock.exchange.country.alpha2)
        local_timestamp = timezone_helper.convert_datetime_to_timezone(self.timestamp, "UTC", timezone)
        return local_timestamp
