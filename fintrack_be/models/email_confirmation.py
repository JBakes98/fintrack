import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from fintrack_be.models.email_address import EmailAddress
from fintrack_be.managers.email_confirmation_manager import EmailConfirmationManager
from fintrack_be.utils import email_util
from fintrack_be.signals import user as signals


class EmailConfirmation(models.Model):

    email_address = models.ForeignKey(EmailAddress, verbose_name=_('e-mail address'), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_('created'), default=timezone.now)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)

    objects = EmailConfirmationManager()

    class Meta:
        verbose_name = _("email confirmation")
        verbose_name_plural = _("email confirmations")

    def __str__(self):
        return "confirmation for %s" % self.email_address

    @classmethod
    def create(cls, email_address):
        key = get_random_string(64).lower()
        return cls._default_manager.create(email_address=email_address, key=key)

    def key_expired(self):
        expiration_date = self.sent \
            + datetime.timedelta(days=settings.EMAIL_CONFIRMATION_EXPIRE_DAYS)
        return expiration_date <= timezone.now()
    key_expired.boolean = True

    def confirm(self, request):
        if not self.key_expired() and not self.email_address.verified:
            email_address = self.email_address
            email_util.confirm_email(request, email_address)
            signals.email_confirmed.send(sender=self.__class__, request=request, email_address=email_address)
            return email_address

    def send(self, request=None, signup=False):
        email_util.send_confirmation_mail(request, signup, emailconfirmation=self)
        self.sent = timezone.now()
        self.save()
        signals.email_confirmation_sent.send(sender=self.__class__, request=request, confirmation=self, signup=signup)