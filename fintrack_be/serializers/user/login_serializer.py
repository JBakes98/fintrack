from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

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

            if not user.verified:
                raise serializers.ValidationError(_('E-mail is not verified.'))

            attrs['user'] = user
            return attrs

        else:
            msg = _("Must Include email and password.")
            raise serializers.ValidationError(msg)