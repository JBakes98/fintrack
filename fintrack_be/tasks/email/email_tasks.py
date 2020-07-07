from __future__ import absolute_import, unicode_literals
from celery.task import task
from fintrack_be.models import EmailTemplate, MailList


@task()
def send_email(*args, **kwargs):
    EmailTemplate.send(*args, **kwargs)


@task()
def send_mail_list(mail_list_id):
    mail_list = MailList.objects.get(pk=mail_list_id)
    for user in mail_list.recipients.all():
        EmailTemplate.send(mail_list.template.template_key,
                           emails=[user.email, ],
                           context={
                               'stocks': user.favourite_stocks.all(),
                               'user': user
                           }
                           ),
