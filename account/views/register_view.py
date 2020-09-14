from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.serializers import RegisterSerializer, TokenSerializer
from account.services import AccountService


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    token_model = Token

    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_serializer(self):
        response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        account_service = AccountService()
        self.token = account_service.create_user_token(self.user.pk)

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class(instance=self.token,
                                      context={'request': self.request})
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)

        return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)
