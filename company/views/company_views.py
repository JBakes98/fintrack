from django.db.models import OuterRef, Subquery, Q
from django.http import Http404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from company.models import Company
from company.serializers import CompanySerializer
from stock.models import Stock, StockPriceData
from stock.serializers import BasicStockSerializer
from fintrack.permissions import IsVerified


class CompanyListView(generics.ListAPIView):
    """
    Get a list of all Company instances, User must be Authenticated and have
    a verified User Email to use API.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CompanySerializer

    def get_queryset(self):
        query_params = {'industry__sector__name': self.request.query_params.get('sector', None),
                        'industry__name': self.request.query_params.get('industry', None)}
        arguments = {}

        # Iterate through request parameters and create dict to apply to queryset
        for k, v in query_params.items():
            if v:
                arguments[k] = v

        return Company.objects.filter(**arguments)


class CompanyDetailView(APIView):
    """
    Retrieve a Company instance, User must be Authenticated and have
    a verified User Email to use API.
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, name):
        try:
            return Company.objects.get(Q(short_name=name) | Q(long_name=name))
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        company = self.get_object(name)
        serializer = CompanySerializer(company)
        return Response(serializer.data)


class CompanySharesListView(generics.ListAPIView):
    """
    Retrieve a Companies listed Stocks, User must be Authenticated and have
    a verified User Email to use API.
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