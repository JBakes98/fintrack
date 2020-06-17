from rest_framework import serializers
from fintrack_be.models import Exchange



class ExchangeSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(source='country.alpha2')

    class Meta:
        model = Exchange
        fields = ('id',
                  'symbol',
                  'name',
                  'opening_time',
                  'closing_time',
                  'market_local_time',
                  'market_open',
                  'country_code',
                  'timezone',
                  'get_stock_count')
