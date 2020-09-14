from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class StockWatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('stock_watchlist',)
        depth = 1
        read_only_fields = ('stock_watchlist', )
