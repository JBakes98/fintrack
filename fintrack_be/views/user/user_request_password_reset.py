from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.helpers import user_token
from fintrack_be.models import User
from fintrack_be.serializers import UserSerializer
from fintrack_be.tasks.email import send_email
from fintrack_be.throttles import OncePerHourUserThrottle


class RequestUserPasswordReset(APIView):
    # throttle_classes = [OncePerHourUserThrottle]

    def post(self, request, format=None):
        """
        Method for User to request an account password reset email, the user must post
        the accounts email, and it be a valid email registered to an account on the system.
        """
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            current_site = get_current_site(self.request)
            send_email.delay('account-password-reset',
                             emails=[user.email, ],
                             context={
                                 'domain': current_site.domain,
                                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                 'token': user_token.make_token(user),
                                 'user': UserSerializer(user).data
                             }
                             )
            return Response('Reset email sent to users email')
        except User.DoesNotExist:
            return Response('Invalid email')
