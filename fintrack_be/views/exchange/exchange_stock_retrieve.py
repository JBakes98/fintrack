from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Exchange
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import ExchangeStockSerializer


class ExchangeStockRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeStockSerializer

    def get_object(self):
        symbol = self.kwargs['symbol']
        return get_object_or_404(Exchange, symbol=symbol)