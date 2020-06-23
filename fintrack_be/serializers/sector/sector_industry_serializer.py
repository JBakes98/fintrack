from rest_framework import serializers
from fintrack_be.models import Sector


class SectorIndustrySerializer(serializers.ModelSerializer):
    sector_industries = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sector
        fields = ['id', 'name', 'sector_industries']