from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from fintrack_be.utils import email_util
from fintrack_be.utils import password_util
from fintrack_be.utils import user_util


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if email and email_util.email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        print(password)
        return password_util.clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }

    def save(self, request):
        user = user_util.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user_util.save_user(request, user, self)
        self.custom_signup(request, user)
        user_util.setup_user_email(request, user, [])
        return user