from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsVerified
from sector.models import Sector
from sector.serializers import SectorIndustrySerializer


class SectorIndustryListView(generics.ListAPIView):
    """
    Get a list of Industry instances under a specific Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = SectorIndustrySerializer
    queryset = Sector.objects.all()