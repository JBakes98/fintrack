from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from fintrack_be.models import Stock
from fintrack_be.serializers.stock import StockSerializer
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

    def list(self, request, *args, **kwargs):
        query_params = {'company__short_name': self.request.query_params.get('company', None),
                        'company__industry__sector__name': self.request.query_params.get('sector', None),
                        'company__industry__name': self.request.query_params.get('industry', None)}
        arguments = {}

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        queryset = Stock.objects.filter(**arguments).order_by('ticker')
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
