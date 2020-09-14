from rest_framework import serializers
from industry.models import Industry


class IndustryCompanySerializer(serializers.ModelSerializer):
    industry_companies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Industry
        fields = ['id', 'name', 'industry_companies']
