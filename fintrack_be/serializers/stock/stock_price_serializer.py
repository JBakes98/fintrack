from rest_framework import serializers
from fintrack_be.models import StockPriceData, Stock


class StockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.SlugRelatedField(many=False,
                                         read_only=False,
                                         queryset=Stock.objects.all(),
                                         slug_field='ticker')

    class Meta:
        model = StockPriceData
        fields = ('id',
                  'timestamp',
                  'stock',
                  'high',
                  'low',
                  'open',
                  'close',
                  'volume',
                  'change',
                  'change_perc')
