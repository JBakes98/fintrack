from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from country.models import Country
from country.serializers import CountrySerializer
from account.permissions import IsVerified


class CountryViewSet(viewsets.ModelViewSet):
    """
    Country ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Countries or Retrieve specific Country


    The User must be a Verified Admin User to use this methods
    POST - Create new Country
    PUT - Fully update existing Country
    PATCH - Partially update existing Country
    DELETE - Delete existing Country
    """
    serializer_class = CountrySerializer
    lookup_field = 'alpha2'

    def get_queryset(self):
        return Country.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
