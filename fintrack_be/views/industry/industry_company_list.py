from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Industry
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import IndustryCompanySerializer


class IndustryCompanyListView(generics.ListAPIView):
    """
    Get an Industry instances Companies
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustryCompanySerializer
    queryset = Industry.objects.all()
