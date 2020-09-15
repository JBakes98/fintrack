from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from account.services import LoginUserAccount

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        # Check if all fields are provided
        if all(credentials.values()):
            usecase = LoginUserAccount(**credentials)
            return usecase.execute()
        else:
            msg = _("Must Include email and password.")
            raise serializers.ValidationError(msg)