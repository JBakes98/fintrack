from __future__ import absolute_import, unicode_literals
from celery.task import task
from fintrack_be.models import EmailTemplate


@task()
def send_email(*args, **kwargs):
    return EmailTemplate.send(*args, **kwargs)

