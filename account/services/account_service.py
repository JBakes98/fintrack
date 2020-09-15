import datetime

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from account.models import User
from account.services import AccountVerificationEmail
from account.exceptions import EmailAlreadyExistsError


class AccountService:
    def __init__(self, first_name=None, last_name=None, email=None, password=None):
        # Set the internal state for the operation
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password

    def register(self):
        """
        Function to create a user account and send the account email verification
        :return: The newly creates User Account
        """
        self.valid_data()
        user_account = User.objects.factory_user_account(
            email=self._email,
            password=self._password,
            first_name=self._first_name,
            last_name=self._last_name)
        AccountVerificationEmail(to_email=user_account.email).send()
        return user_account

    def login(self):
        """
        Function for loging in existing users to their accounts and check there account
        is in a valid state.
        """
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

    def create_user_token(self):
        """
        Function used to create a users auth token when signing in.
        :param user_id: User Id to create their auth token
        :return: The users auth token
        """
        user = self._get_account()
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()
        return token

    def valid_data(self):
        """
        This is a public method that allows clients of the object to
        validate the data before to execute the use case
        """
        account_qs = self._get_account()

        if account_qs:
            # Raise error
            error_msg = (
                'There is another account registered with {}. '
                'Please use another email.'
            ).format(self._email)

            raise EmailAlreadyExistsError(_(error_msg))
        return True

    def _get_account(self):
        """
        Internal method used to get the User model from the email address
        """
        return User.objects.get(email=self._email)
