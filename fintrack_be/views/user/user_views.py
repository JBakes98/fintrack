from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from fintrack_be.models import User
from fintrack_be.tasks.email.email_tasks import send_email
from fintrack_be.helpers.token_helper import user_token
from fintrack_be.serializers import UserSerializer, RegisterUserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        current_site = get_current_site(self.request)
        subject = 'Authenticate your FinTrack Account'
        message = render_to_string('activation_request.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': user_token.make_token(user)
        })
        send_email.delay(subject, message, [user.email, ])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        self.request.user.is_active = False
        self.request.user.is_verified = False
        request.user.save()
        Token.objects.get(user_id=request.user.pk).delete()

        return Response('User deleted', status=status.HTTP_202_ACCEPTED)



