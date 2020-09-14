from rest_framework import serializers
from country.models import Country


class CountryExchangeSerializer(serializers.ModelSerializer):
    country_exchanges = serializers.StringRelatedField(many=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'alpha2', 'alpha3', 'numeric', 'country_exchanges']