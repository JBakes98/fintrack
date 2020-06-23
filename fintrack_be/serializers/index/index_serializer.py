from rest_framework import serializers
from fintrack_be.models import Index


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
