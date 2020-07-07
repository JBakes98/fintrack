from rest_framework import serializers

from fintrack_be.models import User


class UserWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('favourite_stocks',)
        depth = 1
        read_only_fields = ('favourite_stocks', )
