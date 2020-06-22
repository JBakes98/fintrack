from rest_framework import serializers
from index.models import Index, IndexConstituents
from stock.serializers import BasicStockSerializer


class IndexSerializer(serializers.ModelSerializer):
    constituents = serializers.SlugRelatedField(many=True,
                                                read_only=True,
                                                slug_field='ticker')

    class Meta:
        model = Index
        fields = ('id',
                  'symbol',
                  'name',
                  'constituents_count',
                  'constituents')


class IndexCorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('get_index_constituent_correlation', )
