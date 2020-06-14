from rest_framework import serializers
from fintrack_be.models import Company


class CompanySerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source='industry.name')
    sector_name = serializers.CharField(source='industry.sector.name')

    class Meta:
        model = Company
        fields = ('short_name',
                  'long_name',
                  'business_summary',
                  'industry_name',
                  'sector_name')
