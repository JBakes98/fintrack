from decimal import Decimal
from django.db import models
from index.models.index import Index

ONEm = "1m"
ONEh = "1h"
ONEd = "1d"
ONEw = "1w"
ONEM = "1M"
ONEy = "1y"

INTERVAL_OPTIONS = (
        (ONEm, "1m"),
        (ONEh, "1h"),
        (ONEd, "1d"),
        (ONEw, "1w"),
        (ONEM, "1M"),
        (ONEy, "1y"),
    )


BUY = "BUY"
SELL = "SELL"
HOLD = "HOLD"

PREDICTION_OPTIONS = (
    (BUY, "BUY"),
    (SELL, "SELL"),
    (HOLD, "HOLD"),
)


class IndexPriceData(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    index = models.ForeignKey(Index, related_name='index_data', on_delete=models.CASCADE)

    high = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    low = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    open = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    close = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    volume = models.BigIntegerField(blank=True, null=True)

    change = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    change_perc = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))

    class Meta:
        verbose_name = 'Index Price Data'
        verbose_name_plural = 'Indices Price Data'
        db_table = 'index_price'

    def __str__(self):
        string = self.index.symbol + ' ' + str(self.timestamp)
        return string

    class Meta:
        indexes = [
            models.Index(fields=['timestamp', 'index']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['index', 'timestamp'], name='unique_index_data')
        ]