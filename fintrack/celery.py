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
    from fintrack_be.models import MailList
    from fintrack_be.tasks.exchange.exchange_tasks import get_exchanges_day_data
    from fintrack_be.tasks.email.email_tasks import send_mail_list

    exchanges = Exchange.objects.all()
    for exchange in exchanges:
        close = exchange.get_market_close_utc()
        sender.add_periodic_task(
            crontab(hour=close.hour, minute=close.minute, day_of_week='mon-fri'),
            get_exchanges_day_data.s(exchange.symbol),
        )

    mail_lists = MailList.objects.all()
    for mail_list in mail_lists:
        sender.add_periodic_task(
            crontab(hour=mail_list.send_time.hour,
                    minute=mail_list.send_time.minute,
                    day_of_week=mail_list.send_days),
            send_mail_list.s(mail_list.pk),
        )

    # sender.add_periodic_task(
    #     crontab(minute='*/1', day_of_week='mon-fri'),
    #     get_exchanges_day_data.s('NASDAQ'),
    # )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
