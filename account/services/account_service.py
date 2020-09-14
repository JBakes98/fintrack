import datetime

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class AccountService:
    @staticmethod
    def get_user(user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
            return user
        except UserModel.DoesNotExist as e:
            raise e

    def create_user_token(self, user_id):
        user = self.get_user(user_id)
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()

        return token

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
