from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from fintrack_be.models import User
from fintrack_be.permissions import IsUser, IsVerified
from fintrack_be.serializers import UserSerializer
from fintrack_be.services.user.user_service import UserService


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
    lookup_field = 'email'
    lookup_value_regex = '[^/]+'

    def get_permissions(self):
        # Allow non-authenticated User to create via POST method
        if self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        elif self.action == 'retrieve' or self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [IsUser | IsAdminUser]
        elif self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, IsVerified]

        return super(self.__class__, self).get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.data)
            user_service = UserService()
            user_service.create_user_token(user.pk)
            user_service.send_verification_email(user.pk, request)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        user.is_active = False
        user.is_verified = False
        user.is_staff = False
        user.save()

        try:
            Token.objects.get(user_id=user.pk).delete()
        except Token.DoesNotExist:
            pass

        return Response('User deleted', status=status.HTTP_202_ACCEPTED)
