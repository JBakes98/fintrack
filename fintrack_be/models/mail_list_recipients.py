from django.db import models
from django.utils import timezone

from fintrack_be.models.user import User
from fintrack_be.models.mail_list import MailList


class MailListRecipients(models.Model):
    mail_list = models.ForeignKey(MailList, on_delete=models.CASCADE, related_name='recipient_mail_list')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mail_list_recipient')
    date_joined = models.DateField(null=False, blank=False, default=timezone.now)
    active = models.BooleanField(null=False, blank=False, default=True)

    class Meta:
        verbose_name = 'Mail List Recipient'
        verbose_name_plural = 'Mail List Recipients'
        ordering = ['mail_list', 'user']

        constraints = [
            models.UniqueConstraint(fields=['mail_list', 'user'], name='mail_list_recipient')
        ]
