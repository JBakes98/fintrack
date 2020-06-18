from rest_framework import serializers
from index.models import Index
from stock.serializers import BasicStockSerializer


class IndexSerializer(serializers.ModelSerializer):
    constituents = BasicStockSerializer(many=True)

    class Meta:
        model = Index
        fields = ('id',
                  'symbol',
                  'name',
                  'get_constituents_count',
                  'constituents')


class IndexCorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('get_index_constituent_correlation', )
