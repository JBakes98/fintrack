from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fintrack_be.models import Index
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import IndexCorrelationSerializer
from fintrack_be.services.index.IndexMachineLearningService import IndexMachineLearningService


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

    def get(self, request, symbol, format=None):
        index = Index.objects.get(symbol=self.get_object(symbol))
        index_service = IndexMachineLearningService()
        df = index_service.get_index_constituent_correlation(index.pk)
        serializer = IndexCorrelationSerializer(df.to_dict())
        print(serializer.data)
        return Response(df.to_json())
