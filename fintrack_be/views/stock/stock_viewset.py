from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from fintrack_be.models import Stock
from fintrack_be.serializers import StockSerializer
from fintrack_be.permissions import IsVerified


class StockViewSet(viewsets.ModelViewSet):
    """
    Stock ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Stocks or Retrieve specific Stock


    The User must be a Verified Admin User to use this methods
    POST - Create new Stock
    PUT - Fully update existing Stock
    PATCH - Partially update existing Stock
    DELETE - Delete existing Stock
    """
    serializer_class = StockSerializer
    lookup_field = 'ticker'
    lookup_value_regex = '[0-9.A-Z]+'

    def get_queryset(self):
        return Stock.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
