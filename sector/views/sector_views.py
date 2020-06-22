from django.db.models import OuterRef, Subquery
from django.http import Http404

from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from industry.serializers import IndustrySerializer
from sector.models import Sector
from sector.serializers import SectorSerializer
from industry.models import Industry
from company.models import Company
from company.serializers import CompanySerializer
from sector.services.sector_service import SectorDto, SectorService
from stock.models import Stock, StockPriceData
from stock.serializers import BasicStockSerializer
from fintrack.permissions import IsVerified


class SectorViewSet(viewsets.ModelViewSet):
    """
    Sector ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Sectors or Retrieve specific Sector


    The User must be a Verified Admin User to use this methods
    POST - Create new Sector
    PUT - Fully update existing Sector
    PATCH - Partially update existing Sector
    DELETE - Delete existing Sector

    """
    serializer_class = SectorSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Sector.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'POST':
            return (IsAdminUser(), IsVerified())
        else:
            return (IsAuthenticated(), IsVerified())


class SectorIndustryListView(generics.ListAPIView):
    """
    Get a list of Industry instances under a specific Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustrySerializer

    def get_queryset(self):
        name = self.kwargs['name']
        return Industry.objects.filter(sector__name=name)


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
