from django.db.models import OuterRef, Subquery
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sector.models import Sector
from industry.models import Industry
from fintrack_be.models import Company, Stock, StockPriceData
from sector.serializers.sector_serializer import SectorSerializer
from fintrack_be.serializers.company_serializer import CompanySerializer
from fintrack_be.serializers.stock_serializer import BasicStockSerializer
from fintrack_be.permissions import IsVerified


class SectorListView(generics.ListAPIView):
    """
    Get a list of Sector instances
    """
    queryset = Sector.objects.all().order_by('name')
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = SectorSerializer


class SectorDetailView(APIView):
    """
    Retrieve a specific Sector instance
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, name):
        try:
            return Sector.objects.get(name=name)
        except Sector.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        sector = self.get_object(name)
        serializer = SectorSerializer(sector)
        return Response(serializer.data)


class SectorCompanyListView(generics.ListAPIView):
    """
    Get a list of Company instances under a specific Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs['name']
        try:
            industries = Industry.objects.filter(sector__name=name)
        except Sector.DoesNotExist:
            raise Http404
        except Industry.DoesNotExist:
            raise Http404

        try:
            companies = Company.objects.filter(industry__in=industries)
            return companies
        except Company.DoesNotExist:
            raise Http404


class SectorStockListView(generics.ListAPIView):
    """
    Get a list of Stock instances in a Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = BasicStockSerializer

    def get_queryset(self):
        name = self.kwargs['name']

        try:
            sector = Sector.objects.get(name=name)
        except Sector.DoesNotExist:
            raise Http404

        try:
            industries = Industry.objects.filter(sector=sector)
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
