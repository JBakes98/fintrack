from django.db.models import OuterRef, Subquery
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.models import Industry, Company, Stock, StockPriceData
from fintrack_be.serializers.industry_serializer import IndustrySerializer
from fintrack_be.serializers.company_serializer import CompanySerializer
from fintrack_be.serializers.stock_serializer import BasicStockSerializer
from fintrack_be.permissions import IsVerified


class IndustryListView(generics.ListAPIView):
    """
    Get a list of all Industry instances
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustrySerializer

    def get_queryset(self):
        query_params = {'sector__name': self.request.query_params.get('sector', None)}
        arguments = {}

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        return Industry.objects.filter(**arguments).order_by('name')


class IndustryDetailView(APIView):
    """
    Retrieve a specific Industry instance
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, name):
        try:
            return Industry.objects.get(name=name)
        except Industry.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        industry = self.get_object(name)
        serializer = IndustrySerializer(industry)
        return Response(serializer.data)


class IndustryCompanyListView(generics.ListAPIView):
    """
    Get an Industry instances Companies
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs['name']

        try:
            industry = Industry.objects.get(name=name)
        except Industry.DoesNotExist:
            raise Http404

        try:
            return Company.objects.filter(industry=industry)
        except Industry.DoesNotExist:
            raise Http404


class IndustryStockListVIew(generics.ListAPIView):
    """
    Get a list of Stock instances in a Industry
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = BasicStockSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        try:
            industries = Industry.objects.filter(name=name)
        except Industry.DoesNotExist:
            raise Http404

        try:
            companies = Company.objects.filter(industry__in=industries)
        except Company.DoesNotExist:
            raise Http404

        try:
            stocks = Stock.objects.filter(company__in=companies).order_by('ticker')
            latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
            return stocks.annotate(price=Subquery(latest_data.values('close')[:1]))
        except Stock.DoesNotExist:
            raise Http404
        except StockPriceData.DoesNotExist:
            raise Http404