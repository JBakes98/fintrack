from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import Position
from fintrack_be.permissions import IsVerified, IsUser
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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Position.objects.all()
        return Position.objects.filter(user=self.request.user)

    def get_permissions(self):
        # Allow non-authenticated User to create via POST method
        if self.action == 'list':
            self.permission_classes = [IsUser | IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [IsUser | IsAdminUser]
        elif self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, IsVerified]

        return super(self.__class__, self).get_permissions()
