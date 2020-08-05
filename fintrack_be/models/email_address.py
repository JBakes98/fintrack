from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from fintrack_be.managers import EmailAddressManager
from fintrack_be.models.email_confirmation_hmac import EmailConfirmationHMAC

UserModel = get_user_model()


class EmailAddress(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='user')
    email = models.EmailField(unique=True, max_length=254, verbose_name=_('email address'))
    verified = models.BooleanField(verbose_name=_('verified'), default=False)
    primary = models.BooleanField(verbose_name=_('primary'), default=False)

    objects = EmailAddressManager()

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")

    def __str__(self):
        return self.email

    def set_as_primary(self, conditional=False):
        old_primary = EmailAddress.objects.get_primary(self.user)
        if old_primary:
            if conditional:
                return False
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        self.user.save()
        return True

    def send_confirmation(self, request=None, signup=False):
        from fintrack_be.models.email_confirmation import EmailConfirmation

        if settings.EMAIL_CONFIRMATION_HMAC:
            confirmation = EmailConfirmationHMAC(self)
        else:
            confirmation = EmailConfirmation.create(self)
        confirmation.send(request, signup=signup)
        return confirmation

    def change(self, request, new_email, confirm=True):
        """
        Given a new email address, change self and re-confirm.
        """
        with transaction.atomic():
            self.user.save()
            self.email = new_email
            self.verified = False
            self.save()
            if confirm:
                self.send_confirmation(request)