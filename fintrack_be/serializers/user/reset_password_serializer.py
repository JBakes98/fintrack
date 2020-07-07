from rest_framework import serializers

from fintrack_be.models import User


class ResetPasswordSerializer(serializers.Serializer):
    model = User

    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
