from rest_framework import serializers
from fintrack_be.models import Country


class CountryExchangeSerializer(serializers.ModelSerializer):
    country_exchanges = serializers.StringRelatedField(many=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'alpha2', 'alpha3', 'numeric', 'country_exchanges']
