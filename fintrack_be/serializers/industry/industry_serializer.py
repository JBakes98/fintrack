from rest_framework import serializers
from fintrack_be.models import Sector
from fintrack_be.models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    sector = serializers.SlugRelatedField(many=False,
                                          read_only=False,
                                          queryset=Sector.objects.all(),
                                          slug_field='name')

    class Meta:
        model = Industry
        fields = ['id', 'name', 'sector', 'company_count']
