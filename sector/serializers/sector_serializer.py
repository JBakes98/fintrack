from rest_framework import serializers
from sector.models import Sector


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class SectorIndustriesSerializer(serializers.ModelSerializer):
    industries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sector

