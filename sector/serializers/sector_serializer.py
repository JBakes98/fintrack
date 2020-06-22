from rest_framework import serializers
from sector.models import Sector


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'industry_count', 'company_count']


class SectorIndustrySerializer(serializers.ModelSerializer):
    sector_industries = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sector
        fields = ['id', 'name', 'sector_industries']