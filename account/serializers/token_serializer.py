from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key', )
