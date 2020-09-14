from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


class AccountVerificationSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uidb64']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.user.is_verified = True
        self.user.verified = timezone.now()
        self.user.save()



        return attrs

    def save(self):
        return self.user