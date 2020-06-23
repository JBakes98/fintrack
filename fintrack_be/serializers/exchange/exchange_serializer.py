from rest_framework import serializers

from fintrack_be.models import Country
from fintrack_be.models import Exchange


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
