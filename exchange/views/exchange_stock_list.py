from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsVerified
from exchange.models import Exchange
from exchange.serializers import ExchangeStockSerializer


class ExchangeStockListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeStockSerializer
    queryset = Exchange.objects.all()
