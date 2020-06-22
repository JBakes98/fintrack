from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from country.models import Country
from country.serializer.country_serializer import CountrySerializer, CountryExchangeSerializer
from fintrack.permissions import IsVerified


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

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())


class CountryExchangeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CountryExchangeSerializer
    queryset = Country.objects.all()


class CountryExchangeRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsVerified]
    serializer_class = CountryExchangeSerializer

    def get_object(self):
        alpha2 = self.kwargs['alpha2']
        return get_object_or_404(Country, alpha2=alpha2)
