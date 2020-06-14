import uuid
from decimal import Decimal

from django.db import models

from fintrack_be.models import Stock

BUY = 'BUY'
SELL = 'SELL'

POSITION_DIRECTION = (
    (BUY, 'BUY'),
    (SELL, 'SELL')
)


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instrument = models.ForeignKey(Stock, related_name='position_instrument', on_delete=models.CASCADE)

    open_date = models.DateTimeField(null=False, blank=False)
    close_date = models.DateTimeField(null=True, blank=True)
    open_price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    close_price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00))
    result = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    direction = models.CharField(max_length=4, choices=POSITION_DIRECTION, default=BUY)

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        db_table = 'position'

        indexes = [
            models.Index(fields=['id', 'instrument']),
        ]

    def __str__(self):
        return self.id

