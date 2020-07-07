from rest_framework import serializers
from fintrack_be.models import Industry


class IndustryCompanySerializer(serializers.ModelSerializer):
    industry_companies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Industry
        fields = ['id', 'name', 'industry_companies']
