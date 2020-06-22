from rest_framework import serializers
from stock.models import Stock


class BasicStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('ticker',
                  'name',
                  'exchange_symbol',
                  'company_name')