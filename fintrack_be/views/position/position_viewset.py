from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import Position
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.position.position_serializer import PositionSerializer


class PositionViewSet(viewsets.ModelViewSet):
    """
    Position ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Indices or Retrieve specific Position


    The User must be a Verified Admin User to use this methods
    POST - Create new Position
    PUT - Fully update existing Position
    PATCH - Partially update existing Position
    DELETE - Delete existing Position
    """
    serializer_class = PositionSerializer
    lookup_field = 'symbol'

    def get_queryset(self):
        return Position.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
