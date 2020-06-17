from __future__ import absolute_import, unicode_literals
from django.core.mail import EmailMessage
from fintrack.celery import app


@app.task()
def send_email(subject, message, recipient):
    email = EmailMessage(subject, message, to=recipient)
    email.send()
