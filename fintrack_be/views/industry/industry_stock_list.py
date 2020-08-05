from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Industry, Company, Stock
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.stock import StockSerializer


class IndustryStockListVIew(generics.ListAPIView):
    """
    Get a list of Stock instances in a Industry
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        try:
            industries = Industry.objects.filter(name=name)
        except Industry.DoesNotExist:
            raise Http404

        try:
            companies = Company.objects.filter(industry__in=industries)
        except Company.DoesNotExist:
            raise Http404

        try:
            return Stock.objects.filter(company__in=companies).order_by('ticker')
        except Stock.DoesNotExist:
            raise Http404
