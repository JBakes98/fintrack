import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from user.models import User
from fintrack_be.tasks.email_tasks import send_email
from user.token_helper import user_token
from user.serializers.user_serializer import UserSerializer, RegisterUserSerializer
from fintrack_be.throttles import OncePerHourUserThrottle


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        """
        View for handling the User authentication emails that are send upon user signup.
        :param uidb64: This is the User objects UID encoded
        :param token: This is the User objects Token to authenticate the Account
        :return: Simple JSON response to say what the result is
        """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None

        if user is not None and user_token.check_token(user, token):
            # If valid set the user to verified
            user.is_verified = True
            user.verified = timezone.now()
            user.save()

            return Response({'User email now verified'})
        return Response({'Invalid authentication link'})


class UserRequestEmailVerificationAPIView(APIView):
    throttle_classes = [OncePerHourUserThrottle]
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        """
        Method for User to request an account verification email to be sent to
        the accounts email address to verify account.
        :param request:
        :return: JSON response
        """
        user = self.request.user
        if not user.is_verified:
            current_site = get_current_site(self.request)
            subject = 'Authenticate your FinTrack Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_token.make_token(user)
            })
            send_email.delay(subject, message, [user.email, ])

            return Response('Email sent', status=status.HTTP_202_ACCEPTED)
        return Response('User account already verified', status=status.HTTP_200_OK)


class RequestUserPasswordReset(APIView):
    throttle_classes = [OncePerHourUserThrottle]

    def post(self, request, format=None):
        """
        Method for User to request an account password reset email, the user must post
        the accounts email, and it be a valid email registered to an account on the system.
        :param request: Request that contains User email
        :return: JSON response data
        """
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            current_site = get_current_site(self.request)
            subject = 'FinTrack Password Reset'
            message = render_to_string('password_reset_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_token.make_token(user)
            })
            send_email.delay(subject, message, [user.email, ])

            return Response('Reset email sent to users email')

        except User.DoesNotExist:
            return Response('Invalid email')


class UserPasswordResetView(APIView):
    def post(self, request, uidb64, token):
        """
        Method used to reset the users password, the URL contains the users
        encoded id and the required token to authenticate the change. The password
        :param request:
        :param uidb64:
        :param token:
        :return:
        """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response('User not found')

        if user_token.check_token(user, token):
            password = request.POST.get('password')
            user.set_password(password)
            user.save()

            return Response('User password updated')
        return Response('Invalid token')


class UserDetailAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


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


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.update_or_create(user=user)

            if not created and token.created < timezone.now() - datetime.timedelta(hours=24):
                token.delete()
                token = Token.objects.create(user=user)
                token.created = timezone.now()
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

