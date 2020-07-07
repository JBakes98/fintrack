from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Sector
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import SectorIndustrySerializer


class SectorIndustryListView(generics.ListAPIView):
    """
    Get a list of Industry instances under a specific Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = SectorIndustrySerializer
    queryset = Sector.objects.all()