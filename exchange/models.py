import datetime
import json

import pytz
from django.db import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from exchange.managers import ExchangeManager
from exchange.helpers import timezone_helper as tz_help
from country.models import Country


class Exchange(models.Model):
    symbol = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=250, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='country_exchanges')
    timezone = models.CharField(max_length=50, blank=False, null=False, default='BST')
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    objects = ExchangeManager()

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchanges'
        ordering = ['symbol', ]

    def __str__(self):
        return self.symbol

    def save(self, silent=False, *args, **kwargs):
        super(Exchange, self).save(*args, **kwargs)
        cron_schedule = CrontabSchedule.objects.create(minute=self.get_market_close_utc.minute,
                                                       hour=self.get_market_close_utc.hour,
                                                       day_of_week='mon-fri')
        task = PeriodicTask.objects.create(crontab=cron_schedule,
                                    name='{}_refresh_stock_data'.format(self.symbol),
                                    task='get_exchanges_day_data',
                                    kwargs=json.dumps({
                                        'exchange_symbol': self.symbol,
                                    })
                                    )
        task.save()

    def delete(self, using=None, keep_parents=False):
        task = PeriodicTask.objects.get(name='{}_refresh_stock_data'.format(self.symbol))
        task.delete()
        super(Exchange, self).delete()

    @property
    def stock_count(self):
        """
        Method that returns the number of Stocks on this Exchange
        :return: Number of Stocks
        """
        return self.exchange_stocks.count()

    @property
    def listed_stocks(self):
        """
        Method that returns all of the Stocks on this Exchange
        """
        return self.exchange_stocks.all()

    @property
    def market_local_time(self):
        """
        Method that gets the markets local time
        """
        try:
            timezone = tz_help.get_timezone(self.timezone, self.country.alpha2)
            pytz_timezone = pytz.timezone(timezone)
            return datetime.datetime.now(pytz_timezone)
        except AttributeError:
            return 'N/A'

    @property
    def market_open(self):
        """
        Method that checks if the market is open
        """
        try:
            timezone = tz_help.get_timezone(self.timezone, self.country.alpha2)
            pytz_timezone = pytz.timezone(timezone)
            exchange_time = datetime.datetime.now(pytz_timezone)

            if exchange_time.isoweekday() in range(1, 6):
                if self.opening_time <= exchange_time.time() <= self.closing_time:
                    return True
            return False
        except AttributeError:
            return 'N/A'

    @property
    def get_market_close_utc(self):
        """
        Method that get the close time of market in UTC
        :return: UTC time of market close
        """
        timezone = tz_help.get_timezone(self.timezone, self.country.alpha2)
        utc_close = tz_help.convert_time_to_timezone(self.closing_time, timezone, "UTC")
        return utc_close
