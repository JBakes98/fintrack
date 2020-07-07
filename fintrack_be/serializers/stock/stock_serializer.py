from rest_framework import serializers
from fintrack_be.models import Company
from fintrack_be.models import Exchange
from fintrack_be.models import Stock


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
