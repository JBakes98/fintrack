from django.conf import settings
from django.core import signing

from fintrack_be.utils import email as utils
from fintrack_be.signals import user as signals


class EmailConfirmationHMAC:
    def __init__(self, email_address):
        self.email_address = email_address

    @property
    def key(self):
        return signing.dumps(obj=self.email_address.pk, salt=settings.SALT)

    @classmethod
    def from_key(cls, key):
        from fintrack_be.models.email_address import EmailAddress

        try:
            max_age = (
                60 * 60 * 24 * settings.EMAIL_CONFIRMATION_EXPIRE_DAYS)
            pk = signing.loads(key, max_age=max_age, salt=settings.SALT)
            ret = EmailConfirmationHMAC(EmailAddress.objects.get(pk=pk))
        except (signing.SignatureExpired,
                signing.BadSignature,
                EmailAddress.DoesNotExist):
            ret = None
        return ret

    def confirm(self, request):
        if not self.email_address.verified:
            email_address = self.email_address
            utils.confirm_email(request, email_address)
            signals.email_confirmed.send(sender=self.__class__,
                                         request=request,
                                         email_address=email_address)
            return email_address

    def send(self, request=None, signup=False):
        utils.send_confirmation_mail(request, self, signup)
        signals.email_confirmation_sent.send(sender=self.__class__,
                                             request=request,
                                             confirmation=self,
                                             signup=signup)
