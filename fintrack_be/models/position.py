import uuid
from decimal import Decimal
from django.db import models

from fintrack_be.models import User
from fintrack_be.models.stock import Stock

BUY = 'BUY'
SELL = 'SELL'

POSITION_DIRECTION = (
    (BUY, 'BUY'),
    (SELL, 'SELL')
)


class Position(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instrument = models.ForeignKey(Stock, related_name='position_stock', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='position_user', on_delete=models.CASCADE)

    open_date = models.DateTimeField(null=False, blank=False)
    close_date = models.DateTimeField(null=True, blank=True)
    open_price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00), null=False, blank=False)
    close_price = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))

    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal(0.00), null=False, blank=False)
    result = models.DecimalField(max_digits=15, decimal_places=4, default=Decimal(0.00))
    direction = models.CharField(max_length=4, choices=POSITION_DIRECTION, default=BUY)
    is_open = models.BooleanField(blank=False, null=False, default=True)

    REQUIRED_FIELDS = ['instrument', 'user', 'open_date', 'open_price', 'quantity', 'direction']

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['instrument', ]
        indexes = [
            models.Index(fields=['id', 'instrument', 'user']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['id', 'user', 'instrument'], name='unique_position')
        ]

    def __str__(self):
        return self.id

