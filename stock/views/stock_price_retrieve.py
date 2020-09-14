from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsVerified
from stock.models import StockPriceData
from stock.serializers import StockPriceSerializer


class StockPriceRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceSerializer
    queryset = StockPriceData.objects.all()

