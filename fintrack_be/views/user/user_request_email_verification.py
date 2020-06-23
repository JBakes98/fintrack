from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.helpers import user_token
from fintrack_be.models import User
from fintrack_be.serializers import UserSerializer
from fintrack_be.tasks.email import send_email
from fintrack_be.throttles import OncePerHourUserThrottle


class UserRequestEmailVerificationAPIView(APIView):
    throttle_classes = [OncePerHourUserThrottle]
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request):
        """
        Method for User to request an account verification email to be sent to
        the accounts email address to verify account.
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
            # Need to make this an async task
            send_email.delay(subject, message, [user.email, ])

            return Response('Email sent', status=status.HTTP_202_ACCEPTED)
        return Response('User account already verified', status=status.HTTP_200_OK)
