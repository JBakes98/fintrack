from rest_framework import serializers
from fintrack_be.models import Exchange


class ExchangeStockSerializer(serializers.ModelSerializer):
    exchange_stocks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Exchange
        fields = ['id', 'symbol', 'exchange_stocks']