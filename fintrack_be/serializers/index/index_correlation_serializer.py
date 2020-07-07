from rest_framework import serializers
from fintrack_be.models import Index


class IndexCorrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = ('get_index_constituent_correlation', )
