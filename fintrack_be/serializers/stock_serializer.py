from rest_framework import serializers
from fintrack_be.models import Stock, StockPriceData


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
