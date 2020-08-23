from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from fintrack_be.serializers.user import RegisterSerializer, TokenSerializer
from fintrack_be.services.user.user_service import UserService


class RegisterView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_serializer(self):
        response_serializer = TokenSerializer
        return response_serializer


    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class(instance=self.token,
                                      context={'request': self.request})
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def post(self, request):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.serializer.create()

        return Response({"detail": "User created"})
