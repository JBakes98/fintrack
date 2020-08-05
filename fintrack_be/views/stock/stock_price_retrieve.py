from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import StockPriceData
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.stock import StockPriceSerializer


class StockPriceRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockPriceSerializer
    queryset = StockPriceData.objects.all()

