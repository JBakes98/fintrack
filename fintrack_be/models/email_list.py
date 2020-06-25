from django.db import models

from fintrack_be.models import User
from fintrack_be.models.email_template import EmailTemplate


class EmailList(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='list_email')
    recipients = models.ManyToManyField(User, through='EmailListRecipients', blank=True)
    send_time = models.TimeField(null=True, blank=True)
    send_days = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Email List'
        verbose_name_plural = 'Email Lists'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def recipient_count(self):
        return self.recipients.count()
