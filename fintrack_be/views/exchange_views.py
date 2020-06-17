from django.db.models import OuterRef, Subquery
from django.http import Http404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.models import Exchange, Stock, StockPriceData
from fintrack_be.serializers.exchange_serializer import ExchangeSerializer
from fintrack_be.serializers.stock_serializer import StockSerializer
from fintrack_be.permissions import IsVerified


class ExchangeListView(generics.ListAPIView):
    """
    Retrieve a list of all Exchange instances
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        query_params = {'country__alpha2': self.request.query_params.get('country', None),
                        'timezone': self.request.query_params.get('timezone', None)}
        arguments = {}

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        return Exchange.objects.filter(**arguments).order_by('symbol')


class ExchangeDetailView(APIView):
    """
    Retrieve a specific Exchange instance
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, symbol):
        try:
            return Exchange.objects.get(symbol=symbol)
        except Exchange.DoesNotExist:
            raise Http404

    def get(self, request, symbol, format=None):
        exchange = self.get_object(symbol)
        serializer = ExchangeSerializer(exchange)
        return Response(serializer.data)


class ExchangeStocksList(generics.ListAPIView):
    """
    This view should return a list of all stocks for a specific exchange
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

    def get_queryset(self):
        symbol = self.kwargs['symbol']
        query_params = {'company__industry__sector__name': self.request.query_params.get('sector', None),
                        'company__industry__name': self.request.query_params.get('industry', None)}
        arguments = {}

        try:
            exchange = Exchange.objects.get(symbol=symbol)
        except Exchange.DoesNotExist:
            raise Http404

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        stocks = Stock.objects.filter(exchange=exchange, **arguments)
        latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
        return stocks.annotate(price=Subquery(latest_data.values('close')[:1]),
                               change=Subquery(latest_data.values('change')[:1]),
                               change_perc=Subquery(latest_data.values('change_perc')[:1]),
                               price_date_utc=Subquery(latest_data.values('timestamp')[:1]))
