from rest_framework import serializers
from fintrack_be.models import Company
from fintrack_be.models import Industry


class CompanySerializer(serializers.ModelSerializer):
    industry = serializers.SlugRelatedField(many=False,
                                            read_only=False,
                                            queryset=Industry.objects.all(),
                                            slug_field='name')

    class Meta:
        model = Company
        fields = ['id', 'short_name', 'long_name', 'business_summary', 'industry']
