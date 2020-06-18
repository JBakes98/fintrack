from rest_framework import serializers
from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    exchange_symbol = serializers.CharField(source='exchange.symbol')
    company_name = serializers.CharField(source='company.short_name')
    company_summary = serializers.CharField(source='company.business_summary')
    industry = serializers.CharField(source='company.industry.name')
    sector = serializers.CharField(source='company.industry.sector.name')
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    change = serializers.DecimalField(decimal_places=2, max_digits=15)
    change_perc = serializers.DecimalField(max_digits=15, decimal_places=2)
    price_date_utc = serializers.DateTimeField()

    class Meta:
        model = Stock
        fields = ('ticker',
                  'name',
                  'exchange_symbol',
                  'company_name',
                  'company_summary',
                  'industry',
                  'sector',
                  'price',
                  'change',
                  'change_perc',
                  'price_date_utc')
