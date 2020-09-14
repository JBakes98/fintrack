from rest_framework import serializers
from company.models import Company
from industry.models import Industry


class CompanySerializer(serializers.ModelSerializer):
    industry = serializers.SlugRelatedField(many=False,
                                            read_only=False,
                                            queryset=Industry.objects.all(),
                                            slug_field='name')

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'long_name', 'business_summary', 'industry']
