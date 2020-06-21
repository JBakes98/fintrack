from django.db.models import OuterRef, Subquery
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from sector.models import Sector
from sector.serializers import SectorSerializer
from industry.models import Industry
from company.models import Company
from company.serializers import CompanySerializer
from sector.services.sector_service import SectorDto, SectorService
from stock.models import Stock, StockPriceData
from stock.serializers import BasicStockSerializer
from fintrack.permissions import IsVerified


class SectorListCreateView(generics.ListCreateAPIView):
    """
    Get a list of all Sector instances, this view offers two HTTP methods.

    The User must be Verified to use this method
    GET - List existing Sector

    The User must be a Verified Admin User to use this methods
    POST - Create new Sector

    This views offers GET and POST method handlers.
    """
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'POST':
            return (IsAdminUser(), IsVerified())
        else:
            return (IsAuthenticated(), IsVerified())

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Invoke validation and build service input argument in the form
        # of a Dto (DataTransferObject)
        dto = self._build_dto_from_validated_data(request)
        sector_service = SectorService()

        sector_service.create_sector_Dto(dto)
        return Response({'success': True})

    def _build_dto_from_validated_data(self, request) -> SectorDto:
        serializer = SectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return SectorDto(
            name=data['name'],
        )


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
