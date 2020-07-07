from rest_framework import serializers
from fintrack_be.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'alpha2', 'alpha3', 'numeric']
