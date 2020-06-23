from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Country
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import CountryExchangeSerializer


class CountryExchangeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CountryExchangeSerializer
    queryset = Country.objects.all()
