import datetime
from django.db.models import OuterRef, Subquery
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from stock.models import Stock, StockPriceData, INTERVAL_OPTIONS
from stock.serializers import StockSerializer, StockPriceSerializer
from fintrack.permissions import IsVerified


class StockViewSet(viewsets.ModelViewSet):
    """
    Stock ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Stocks or Retrieve specific Stock


    The User must be a Verified Admin User to use this methods
    POST - Create new Stock
    PUT - Fully update existing Stock
    PATCH - Partially update existing Stock
    DELETE - Delete existing Stock
    """
    serializer_class = StockSerializer
    lookup_field = 'ticker'

    def get_queryset(self):
        return Stock.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())


class StockPriceListView(generics.ListAPIView):
    """
    API view to get the stock price data for a specific Stock instance, client can specify the
    time interval of the data they want through the URL parameter interval=
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        """
        Retrieve a specific Stocks Price instances
        """
        valid_interval = False
        ticker = self.kwargs['ticker']
        interval = self.request.query_params.get('interval', '1d')

        from_date = datetime.datetime.strptime(
            self.request.query_params.get(
                'from',
                '1000-01-01'),
            '%Y-%m-%d')
        to_date = datetime.datetime.strptime(
            self.request.query_params.get(
                'to',
                datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')),
            '%Y-%m-%d')

        if from_date > to_date:
            raise ValidationError(detail='Ensure the from and to date parameters are valid')

        for k, v in INTERVAL_OPTIONS:
            if v == interval:
                valid_interval = True

        if valid_interval is False:
            raise ValidationError(detail='Ensure you have selected a valid data interval')

        return StockPriceData.objects.filter(
            stock__ticker=ticker,
            timestamp__range=[from_date, to_date]
        ).order_by('-timestamp')


class PriceRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceSerializer
    queryset = StockPriceData.objects.all()


class UserFavouriteStockView(APIView):
    permission_classes = (IsAuthenticated, IsVerified)

    def post(self, request, ticker):
        try:
            stock = Stock.objects.get(ticker=ticker)
        except Stock.DoesNotExist:
            return Response('Stock with ticker {} not found'.format(ticker))

        user = request.user
        if User.objects.filter(pk=user.pk, favourite_stocks__pk=stock.pk):
            user.favourite_stocks.remove(stock)
            return Response('{} Removed from favourites'.format(ticker))
        else:
            user.favourite_stocks.add(stock)
            return Response('{} Added to favourites'.format(ticker))
