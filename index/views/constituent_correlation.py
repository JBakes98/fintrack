from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from index.models import Index
from index.services import IndexService
from account.permissions import IsVerified


class IndexCorrelationListView(generics.ListAPIView):
    """
    Retrieve correlation data of an Indices constituents
    """
    permission_classes = (IsAuthenticated, IsVerified)

    def get_object(self, symbol):
        try:
            return Index.objects.get(symbol=symbol)
        except Index.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    def get(self, request, symbol, format=None):
        index_service = IndexService(symbol=self.get_object(symbol))
        df = index_service.get_index_constituent_correlation()
        return Response(df.to_json())
