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
    from fintrack_be.models import Exchange
    from fintrack_be.models import EmailList
    from fintrack_be.tasks.exchange.exchange_tasks import get_exchanges_day_data
    from fintrack_be.tasks.email.email_tasks import send_email

    exchanges = Exchange.objects.all()
    for exchange in exchanges:
        close = exchange.get_market_close_utc()
        sender.add_periodic_task(
            crontab(hour=close.hour, minute=close.minute, day_of_week='mon-fri'),
            get_exchanges_day_data.s(exchange.symbol),
        )

    email_lists = EmailList.objects.all()
    for email_list in email_lists:
        for user in email_list.recipients.all():
            sender.add_periodic_task(
                crontab(hour=email_list.send_time.hour, day_of_week=email_list.send_days),
                send_email.s(email_list.template,
                             emails=[user.email, ],
                             context={
                                 'stocks': user.favourite_stocks.all(),
                                 'user': user
                             }
                             ),
            )

    # sender.add_periodic_task(
    #     crontab(minute='*/1', day_of_week='mon-fri'),
    #     get_exchanges_day_data.s('NASDAQ'),
    # )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
