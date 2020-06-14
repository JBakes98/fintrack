import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserTokenGenerator(PasswordResetTokenGenerator):
    """
    Class used to create the token used in the email verification emails
    sent to users
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.is_verified) +
            six.text_type(user.password) +
            six.text_type(user.last_login)
        )


user_token = UserTokenGenerator()
