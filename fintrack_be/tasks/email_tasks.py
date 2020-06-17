from __future__ import absolute_import, unicode_literals
from celery.task import task
import datetime
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_celery_results.models import TaskResult
from user.models import User


@task()
def send_email(subject, message, recipient):
    email = EmailMessage(subject, message, to=recipient)
    email.send()


@task()
def send_day_tasks_email():
    date = datetime.datetime.today()
    tasks = TaskResult.objects.filter(date_done__month=date.month, date_done__day=date.day).order_by('status')

    subject = 'FinTrack Daily Task Report {}'.format(date)
    html_message = render('daily_task_report.html', {
        'tasks': tasks,
    })
    plain_message = strip_tags(html_message)

    recipients = User.objects.filter(groups__name='celery_task_admin').values_list('email')
    recipients = list(recipients)

    email = EmailMessage(subject, html_message, to=recipients)
    email.content_subtype = 'html'
    email.send()
