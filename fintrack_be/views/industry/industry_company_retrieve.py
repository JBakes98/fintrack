from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Industry
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import IndustryCompanySerializer


class IndustryCompanyRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = IndustryCompanySerializer

    def get_object(self):
        name = self.kwargs['name']
        return get_object_or_404(Industry, name=name)