from rest_framework import serializers

from country.models import Country
from exchange.models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(many=False,
                                           read_only=False,
                                           queryset=Country.objects.all(),
                                           slug_field='alpha2')

    class Meta:
        model = Exchange
        fields = ['id',
                  'symbol',
                  'name',
                  'opening_time',
                  'closing_time',
                  'market_local_time',
                  'market_open',
                  'country',
                  'timezone',
                  'stock_count']
        depth = 1


class ExchangeStockSerializer(serializers.ModelSerializer):
    exchange_stocks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Exchange
        fields = ['id', 'symbol', 'exchange_stocks']
