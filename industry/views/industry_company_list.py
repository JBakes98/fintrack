from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsVerified
from industry.models import Industry
from industry.serializers import IndustryCompanySerializer


class IndustryCompanyListView(generics.ListAPIView):
    """
    Get an Industry instances Companies
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustryCompanySerializer
    queryset = Industry.objects.all()
