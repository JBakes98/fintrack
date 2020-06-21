from rest_framework import serializers
from industry.models import Industry
from sector.serializers import SectorSerializer


class IndustrySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    sector = SectorSerializer()

    def create(self, validated_data):
        return Industry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.sector = validated_data.get('sector', instance.sector)
