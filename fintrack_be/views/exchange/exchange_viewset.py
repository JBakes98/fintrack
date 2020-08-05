from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import Exchange
from fintrack_be.serializers.exchange import ExchangeSerializer
from fintrack_be.permissions import IsVerified


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
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
