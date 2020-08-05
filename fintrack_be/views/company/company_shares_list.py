from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from fintrack_be.models import Stock
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.stock import StockSerializer


class CompanySharesListView(generics.ListAPIView):
    """
    Retrieve a Companies listed Stocks, this view accepts HTTP GET requests only. The reuquest
    User must be authenticated and verified to access the API.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(company__short_name=self.kwargs['name'])