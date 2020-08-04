import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token

from fintrack_be.helpers import user_token
from fintrack_be.models.user import User


class UserService:
    @staticmethod
    def get_user(user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist as e:
            raise e

    def create_user_token(self, user_id):
        user = self.get_user(user_id)
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()

    def send_verification_email(self, user_id, request):
        from fintrack_be.serializers.user.user_serializer import UserSerializer
        from fintrack_be.tasks.email.email_tasks import send_email

        user = self.get_user(user_id)
        current_site = get_current_site(request)
        send_email.delay('account-verification',
                         emails=[user.email, ],
                         context={
                             'domain': current_site.domain,
                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                             'token': user_token.make_token(user),
                             'user': UserSerializer(user).data
                         }
                         )

    def sufficient_funds(self, user_id, value):
        user = self.get_user(user_id)
        return user.funds >= value

    def update_result(self, user_id, value):
        user = self.get_user(user_id)
        user.result += value
        user.save()
        return user.result

    def update_funds(self, user_id, value):
        user = self.get_user(user_id)
        user.funds += value
        user.save()
        return user.funds
