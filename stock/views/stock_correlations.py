from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsVerified
from stock.serializers import StockCorrelationSerializer
from stock.utils import valid_tickers
from stock.services import StockMachineLearningService


class StocksCorrelation(APIView):
    """
    View to get the correlation of posted stocks

    * The users must be verified to use
    """
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request, format=None):
        """
        Post a list of stock tickers and get their price
        correlation

        Example of POST data "stocks" : ["AAPL", "GOOGL"]
        """
        serializer = StockCorrelationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cl_tickers = valid_tickers.check_valid_ticker(serializer.validated_data['stocks'])
        ml = StockMachineLearningService(stocks=cl_tickers)

        return Response(ml.get_stocks_correlation(),
                        status=status.HTTP_202_ACCEPTED)
