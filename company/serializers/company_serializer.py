from rest_framework import serializers
from company.models import Company
from industry.models import Industry
from industry.serializers import IndustrySerializer


class CompanySerializer(serializers.Serializer):
    short_name = serializers.CharField(max_length=255)
    long_name = serializers.CharField(max_length=512)
    business_summary = serializers.CharField()
    industry = serializers.HyperlinkedRelatedField(queryset=Industry.objects.all(), view_name='industry_detail')

    # def create(self, validated_data):
    #     return Company.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.short_name = validated_data.get('short_name', instance.short_name)
    #     instance.long_name = validated_data.get('long_name', instance.long_name)
    #     instance.business_summary = validated_data.get('business_summary', instance.business_summary)
    #     instance.industry = validated_data.get('industry', instance.industry)