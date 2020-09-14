from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsVerified
from sector.models import Sector
from sector.serializers import SectorIndustrySerializer


class SectorIndustryRetrieveView(generics.RetrieveAPIView):
    """
    Get a list of Industry instances under a specific Sector
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = SectorIndustrySerializer

    def get_object(self):
        name = self.kwargs['name']
        return get_object_or_404(Sector, name=name)
