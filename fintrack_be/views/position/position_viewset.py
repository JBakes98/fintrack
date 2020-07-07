from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from fintrack_be.models import Position
from fintrack_be.permissions import IsVerified, IsUser, IsOwner
from fintrack_be.serializers.position.position_serializer import PositionSerializer, PositionCloseSerializer
from fintrack_be.services.position.position_services import PositionService


class PositionViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
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
        if self.action == 'list' or self.action == 'create':
            self.permission_classes = [IsUser | IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated, IsVerified]

        return super(self.__class__, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            position_service = PositionService()
            position_service.open_position(request.user, self.validated_data)
            return Response({"response": "Position opened"}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors)

    @action(name='Close Position', detail=True, methods=['post'], permission_classes=[IsVerified, IsOwner])
    def close_position(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        position = self.get_object()

        if serializer.is_valid():
            position_service = PositionService()
            position_service.close_position(position.pk, serializer.data)
            return Response({"response": "position closed"}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors)
