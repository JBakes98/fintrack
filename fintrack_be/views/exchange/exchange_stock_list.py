from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Exchange
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import ExchangeStockSerializer


class ExchangeStockListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeStockSerializer
    queryset = Exchange.objects.all()
