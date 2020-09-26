from rest_framework import serializers


class StockCorrelationSerializer(serializers.Serializer):
    stocks = serializers.ListField(allow_empty=False, min_length=2)
