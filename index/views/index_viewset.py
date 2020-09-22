from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from index.models import Index
from index.serializers import IndexSerializer
from account.permissions import IsVerified


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