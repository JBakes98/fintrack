from rest_framework import serializers
from sector.models import Sector


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ('id', 'name', 'sub_industry_count', 'sector_constituents')