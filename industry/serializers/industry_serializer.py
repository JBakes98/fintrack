from rest_framework import serializers
from sector.models import Sector
from industry.models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    sector = serializers.SlugRelatedField(many=False,
                                          read_only=False,
                                          queryset=Sector.objects.all(),
                                          slug_field='name')

    class Meta:
        model = Industry
        fields = ['id', 'name', 'sector', 'company_count']


class IndustryCompanySerializer(serializers.ModelSerializer):
    industry_companies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Industry
        fields = ['id', 'name', 'industry_companies']
