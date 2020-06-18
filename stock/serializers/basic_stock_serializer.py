from rest_framework import serializers
from stock.models import Stock


class BasicStockSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.short_name')
    exchange_symbol = serializers.CharField(source='exchange.symbol')
    industry_name = serializers.CharField(source='company.industry.name')

    class Meta:
        model = Stock
        fields = ('ticker',
                  'name',
                  'exchange_symbol',
                  'company_name',
                  'industry_name')