from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fintrack_be.helpers import user_token
from fintrack_be.models import User
from fintrack_be.serializers import ResetPasswordSerializer


class UserPasswordResetView(APIView):
    def post(self, request, uidb64, token):
        """
        Method used to reset the users password, the URL contains the users
        encoded id and the required token to authenticate the change.
        """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'response': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user_token.check_token(user, token):
            serializer = ResetPasswordSerializer(data=request.data)

            if serializer.is_valid():
                if serializer.validated_data['password1'] == serializer.validated_data['password2']:
                    password = serializer.validated_data['password1']
                    user.set_password(password)
                    user.save()

                    return Response({'response': 'User password updated'}, status=status.HTTP_202_ACCEPTED)
                return Response({'response': 'Passwords dont match'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors)
        return Response({'response': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
