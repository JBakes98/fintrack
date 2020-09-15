from django.utils.translation import gettext as _
from account.models import User
from account.services import AccountVerificationEmail
from account.exceptions import EmailAlreadyExistsError


class RegisterUserAccount:
    def __init__(self, first_name, last_name, email, password):
        # Set the internal state for the operation
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._password = password

    def execute(self):
        self.valid_data()
        user_account = User.objects.factory_user_account(
            email=self._email,
            password=self._password,
            first_name=self._first_name,
            last_name=self._last_name)
        AccountVerificationEmail(to_email=user_account.email).send()
        return user_account

    def valid_data(self):
        """
        This is a public method that allows clients of the object to
        validate the data before to execute the use case
        """
        account_qs = User.objects.find_by_email(self._email)

        if account_qs.exists():
            # Raise error
            error_msg = (
                'There is another account registered with {}. '
                'Please use another email.'
            ).format(self._email)

            raise EmailAlreadyExistsError(_(error_msg))
        return True
