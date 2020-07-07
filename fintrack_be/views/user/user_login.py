import datetime

from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


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

            return Response({'token': token.key,
                             'user_id': user.pk,
                             'user_email': user.email})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
