from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.helpers import user_token
from fintrack_be.models import User


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
