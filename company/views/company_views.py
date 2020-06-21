from django.db.models import OuterRef, Subquery, Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from company.models import Company
from company.serializers import CompanySerializer
from company.services.CompanyService import CompanyDto, CompanyService
from stock.models import Stock, StockPriceData
from stock.serializers import BasicStockSerializer
from fintrack.permissions import IsVerified


class CompanyListCreateView(generics.ListCreateAPIView):
    """
    Get a list of all Company instances, this view offers two HTTP methods.

    The User must be Verified to use this method
    GET - List existing Companies

    The User must be a Verified Admin User to use this methods
    POST - Create new Company

    This views offers GET and POST method handlers.
    """
    serializer_class = CompanySerializer

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'POST':
            return (IsAdminUser(), IsVerified())
        else:
            return (IsAuthenticated(), IsVerified())

    def get_queryset(self):
        query_params = {'industry__sector__name': self.request.query_params.get('sector', None),
                        'industry__name': self.request.query_params.get('industry', None)}
        arguments = {}

        # Iterate through request parameters and create dict to apply to queryset
        for k, v in query_params.items():
            if v:
                arguments[k] = v

        return Company.objects.filter(**arguments)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Invoke validation and build service input argument in the form
        # of a DTO (DataTransferObject)
        dto = self._build_dto_from_validated_data(request)
        print('Dto {}'.format(dto))

        company_service = CompanyService()
        try:
            company_service.create_company_Dto(dto)
        except:
            return Response({'success': False}, status=503)

        return Response({'success': True})

    def _build_dto_from_validated_data(self, request) -> CompanyDto:
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return CompanyDto(
            short_name=data['short_name'],
            long_name=data['long_name'],
            business_summary=data['business_summary'],
            industry_id=data['industry'].id,
        )


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoints related to a specific Company instance, this view offers multiple HTTP methods. The
    url takes a companies short or long name to select the respective Company model.

    The User must be a Verified Admin User to use this methods
    POST - create a new Company
    PATCH - partially update the Company
    PUT - fully update the Company
    DELETE - delete the Company from the system

    The User must be Verified to use this method
    GET - get the Company

    """
    serializer_class = CompanySerializer

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'POST' or request_method == 'PUT' or request_method == 'PATCH' or request_method == 'DELETE':
            return (IsAdminUser(), IsVerified())
        else:
            return (IsAuthenticated(), IsVerified())

    def get_object(self):
        name = self.kwargs['name']
        return get_object_or_404(Company, (Q(short_name=name) | Q(long_name=name)))


class CompanySharesListView(generics.ListAPIView):
    """
    Retrieve a Companies listed Stocks, this view accepts HTTP GET requests only. The reuquest
    User must be authenticated and verified to access the API.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = BasicStockSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        try:
            company = Company.objects.get(Q(short_name=name) | Q(long_name=name))
        except Company.DoesNotExist:
            raise Http404
        try:
            stocks = Stock.objects.filter(company=company).order_by('ticker')
            latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
            queryset = stocks.annotate(price=Subquery(latest_data.values('close')[:1]))
            return queryset
        except Stock.DoesNotExist:
            raise Http404