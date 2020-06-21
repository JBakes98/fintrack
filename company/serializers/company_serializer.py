from rest_framework import serializers
from company.models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'id',
            'short_name',
            'long_name',
            'business_summary',
            'industry')

    def create(self, validated_data):
        company = Company(
            short_name=validated_data['short_name'],
            long_name=validated_data['long_name'],
            business_summary=validated_data['business_summary'],
            industry=validated_data['industry']
        )
        company.save()
        return company
