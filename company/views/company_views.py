from django.db.models import OuterRef, Subquery, Q
from django.http import Http404

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from company.models import Company
from company.serializers import CompanySerializer
from stock.models import Stock, StockPriceData
from stock.serializers import StockSerializer
from fintrack.permissions import IsVerified


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Companies or Retrieve specific Company


    The User must be a Verified Admin User to use this methods
    POST - Create new Company
    PUT - Fully update existing Company
    PATCH - Partially update existing Company
    DELETE - Delete existing Company
    """
    serializer_class = CompanySerializer
    lookup_field = 'short_name'
    lookup_value_regex = '[0-9.A-Z]+'

    def get_queryset(self):
        return Company.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())


class CompanySharesListView(generics.ListAPIView):
    """
    Retrieve a Companies listed Stocks, this view accepts HTTP GET requests only. The reuquest
    User must be authenticated and verified to access the API.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

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