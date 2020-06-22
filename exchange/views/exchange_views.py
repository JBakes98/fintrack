from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from exchange.models import Exchange
from exchange.serializers import ExchangeSerializer, ExchangeStockSerializer
from fintrack.permissions import IsVerified


class ExchangeViewSet(viewsets.ModelViewSet):
    """
    Sector ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Sectors or Retrieve specific Sector


    The User must be a Verified Admin User to use this methods
    POST - Create new Sector
    PUT - Fully update existing Sector
    PATCH - Partially update existing Sector
    DELETE - Delete existing Sector
    """
    serializer_class = ExchangeSerializer
    lookup_field = 'symbol'

    def get_queryset(self):
        return Exchange.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'POST':
            return (IsAdminUser(), IsVerified())
        else:
            return (IsAuthenticated(), IsVerified())


class ExchangeStockListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeStockSerializer
    queryset = Exchange.objects.all()


class ExchangeStockRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = ExchangeStockSerializer

    def get_object(self):
        symbol = self.kwargs['symbol']
        return get_object_or_404(Exchange, symbol=symbol)