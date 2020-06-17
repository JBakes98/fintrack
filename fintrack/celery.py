import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fintrack.settings.development')
app = Celery('fintrack')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from exchange.tasks.exchange_tasks import get_exchanges_day_data
    from fintrack_be.models import Exchange

    exchanges = Exchange.objects.all()
    for exchange in exchanges:
        close = exchange.get_market_close_utc()
        sender.add_periodic_task(
            crontab(hour=close.hour, minute=0, day_of_week='mon-fri'),
            get_exchanges_day_data.s(exchange.symbol),
        )

        # sender.add_periodic_task(
        #     crontab(minute='*/1', day_of_week='mon-fri'),
        #     get_exchanges_day_data.s('NASDAQ'),
        # )

    # sender.add_periodic_task(
    #     crontab(minute='*/1'),
    #     get_latest_data_for_open_markets.s(),
    # )

    # sender.add_periodic_task(
    #     crontab(minute='*/1'),
    #     send_day_tasks_email.s(),
    # )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

