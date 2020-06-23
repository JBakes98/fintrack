from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.helpers import user_token
from fintrack_be.models import User


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