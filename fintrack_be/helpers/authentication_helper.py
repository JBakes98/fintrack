import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRES', 24)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        """
        Takes API key and checks if its valid and that the User is authenticated.
        :param key: API key
        :return: The User the Token belongs to and the Token itself
        """
        try:
            token = self.get_model().objects.get(key=key)
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.created < timezone.now() - datetime.timedelta(hours=EXPIRE_HOURS):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
