import datetime
from django.db import models
from django.utils import timezone

from fintrack_be.models.user import User
from fintrack_be.models.email_list import EmailList


class EmailListRecipients(models.Model):
    email_list = models.ForeignKey(EmailList, on_delete=models.CASCADE, related_name='recipient_email_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_list_recipient')
    date_joined = models.DateField(null=False, blank=False, default=timezone.now)
    active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Email List Recipient'
        verbose_name_plural = 'Email List Recipients'
        ordering = ['email_list', 'user']

        constraints = [
            models.UniqueConstraint(fields=['email_list', 'user'], name='email_list_recipient')
        ]
