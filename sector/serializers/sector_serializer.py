from rest_framework import serializers
from sector.models import Sector


class SectorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
