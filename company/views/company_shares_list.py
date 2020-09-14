from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from stock.models import Stock
from stock.serializers import StockSerializer
from account.permissions import IsVerified


class CompanySharesListView(generics.ListAPIView):
    """
    Retrieve a Companies listed Stocks, this view accepts HTTP GET requests only. The reuquest
    User must be authenticated and verified to access the API.
    """
    permission_classes = (IsAuthenticated, IsVerified)
    serializer_class = StockSerializer

    def get_queryset(self):
        return Stock.objects.filter(company__short_name=self.kwargs['name'])