from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from index.models import Index
from index.serializers import IndexSerializer, IndexCorrelationSerializer
from fintrack.permissions import IsVerified
from index.services.IndexMachineLearningService import IndexMachineLearningService


class IndexViewSet(viewsets.ModelViewSet):
    """
    Index ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Indices or Retrieve specific Index


    The User must be a Verified Admin User to use this methods
    POST - Create new Index
    PUT - Fully update existing Index
    PATCH - Partially update existing Index
    DELETE - Delete existing Index
    """
    serializer_class = IndexSerializer
    lookup_field = 'symbol'

    def get_queryset(self):
        return Index.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())


class IndexCorrelationAPIView(generics.ListAPIView):
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
