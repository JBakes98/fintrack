from rest_framework import serializers

from company.models import Company
from exchange.models import Exchange
from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    exchange = serializers.SlugRelatedField(many=False,
                                            read_only=False,
                                            queryset=Exchange.objects.all(),
                                            slug_field='symbol')
    company = serializers.SlugRelatedField(many=False,
                                           read_only=False,
                                           queryset=Company.objects.all(),
                                           slug_field='short_name')

    class Meta:
        model = Stock
        fields = ['id', 'ticker', 'name', 'company', 'exchange', 'latest_price']