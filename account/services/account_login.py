from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from account.services import AccountVerificationEmail


class LoginUserAccount:
    def __init__(self, email, password):
        self._email = email
        self._password = password

    def execute(self):
        user = authenticate(username=self._email, password=self._password)
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        if not user.is_verified:
            # Call account verification email service to send verification email to accounts email
            AccountVerificationEmail(to_email=user.email).send()
            raise ValidationError(_('Account is not verified, please check your email for verification.'))

        return user
