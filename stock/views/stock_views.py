import datetime
from django.db.models import OuterRef, Subquery
from django.http import Http404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from stock.models import Stock, StockPriceData, INTERVAL_OPTIONS
from stock.serializers import StockSerializer, StockPriceDataSerializer
from fintrack.permissions import IsVerified


class StockListView(generics.ListAPIView):
    """
    Get a list of all Stock instances
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

    def get_queryset(self):
        query_params = {'company__short_name': self.request.query_params.get('company', None),
                        'company__industry__sector__name': self.request.query_params.get('sector', None),
                        'company__industry__name': self.request.query_params.get('industry', None)}
        arguments = {}

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        stocks = Stock.objects.filter(**arguments).order_by('ticker')
        latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
        return stocks.annotate(price=Subquery(latest_data.values('close')[:1]),
                               change=Subquery(latest_data.values('change')[:1]),
                               change_perc=Subquery(latest_data.values('change_perc')[:1]),
                               price_date_utc=Subquery(latest_data.values('timestamp')[:1]))


class StockDetailView(APIView):
    """
    Retrieve a stock instance
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, ticker):
        try:
            latest_data = StockPriceData.objects.filter(stock=OuterRef('pk')).order_by('-timestamp')
            stock = Stock.objects.annotate(price=Subquery(latest_data.values('close')[:1]),
                                           change=Subquery(latest_data.values('change')[:1]),
                                           change_perc=Subquery(latest_data.values('change_perc')[:1]),
                                           price_date_utc=Subquery(latest_data.values('timestamp')[:1])
                                           ).get(ticker=ticker)
            return stock
        except Stock.DoesNotExist:
            raise Http404

    def get(self, request, ticker, format=None):
        stock = self.get_object(ticker)
        serializer = StockSerializer(stock)
        return Response(serializer.data)


class AllStockPriceDataListView(generics.ListAPIView):
    """
    THIS ISN'T WORKING!!!
    List all Stock instances Price instances
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceDataSerializer

    def get_queryset(self):
        """
        Retrieve all price data matching the request
        """
        valid_interval = False
        query_params = {'interval': self.request.query_params.get('interval', '1d'),
                        'ticker': self.request.query_params.get('ticker', None)}
        arguments = {}

        # Check whether the Interval parameter is a valid option to query
        for k, v in INTERVAL_OPTIONS:
            if not v == self.request.query_params.get('interval', '1d'):
                raise ValidationError(detail='Ensure you have selected a valid data interval')

        # Iterate through query parameters and if they have a value add them to query arguments
        for k, v in query_params.items():
            if v:
                arguments[k] = v

        return StockPriceData.objects.filter(**arguments).order_by('stock.ticker')


class StockPriceListView(generics.ListAPIView):
    """
    API view to get the stock price data for a specific Stock instance, client can specify the
    time interval of the data they want through the URL parameter interval=
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceDataSerializer

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
