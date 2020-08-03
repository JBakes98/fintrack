from django.db import models

from fintrack_be.models.user import User
from fintrack_be.models.email_template import EmailTemplate


class MailList(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='mail_list_template')
    recipients = models.ManyToManyField(User, through='MailListRecipients', blank=True)
    send_time = models.TimeField(null=True, blank=True)
    send_days = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Mail List'
        verbose_name_plural = 'Mail Lists'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def recipient_count(self):
        return self.recipients.count()
