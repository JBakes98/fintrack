from rest_framework import serializers
from stock.models import StockPriceData


class StockPriceDataSerializer(serializers.ModelSerializer):
    stock_symbol = serializers.CharField(source='stock.ticker')

    class Meta:
        model = StockPriceData
        fields = ('timestamp',
                  'timestamp_in_market_time',
                  'stock_symbol',
                  'high',
                  'low',
                  'open',
                  'close',
                  'volume',
                  'change',
                  'change_perc')
