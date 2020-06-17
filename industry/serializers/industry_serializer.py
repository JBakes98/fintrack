from rest_framework import serializers
from industry.models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name')

    class Meta:
        model = Industry
        fields = ('id', 'name', 'sector_name', 'industry_company_count')