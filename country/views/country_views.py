from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from country.models import Country
from country.serializer.country_serializer import CountrySerializer
from fintrack.permissions import IsVerified


class CountryListView(generics.ListAPIView):
    """
    Get a list of all Country instances.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = CountrySerializer

    def get_queryset(self):
        return Country.objects.all().order_by('name')

