import datetime

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import StockPriceData
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import StockPriceSerializer


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