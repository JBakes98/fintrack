from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from account.services import AccountService

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        user = None

        # Check if all fields are provided
        if all(credentials.values()):
            user = authenticate(**credentials)

            # Did we get back an active user?
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.ValidationError(msg)

            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)

            if not user.is_verified:
                request = self.context.get('request')
                # Set some values to trigger the send_email method.
                opts = {
                    'use_https': request.is_secure(),
                    'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
                    'request': request,
                    'to_email': user.email,
                }

                AccountService.send_verification_email(**opts)

                raise serializers.ValidationError(_('Account is not verified, please check your email for verification.'))

            attrs['user'] = user
            return attrs

        else:
            msg = _("Must Include email and password.")
            raise serializers.ValidationError(msg)