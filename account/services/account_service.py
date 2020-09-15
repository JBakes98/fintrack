import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token
from account.utils import email_util


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
        """
        Function used to create a users auth token when signing in.
        :param user_id: User Id to create their auth token
        :return: The users auth token
        """
        user = self.get_user(user_id)
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()
        return token

        def sufficient_funds(self, user_id, value):
            """
            Checks that the user has sufficient funds in their account to a value.
            :param user_id: The users ID to check funds
            :param value: The value thats to be checked if they have sufficient funds for
            """
            user = self.get_user(user_id)
            return user.funds >= value

        def update_result(self, user_id, value):
            """
            Updates the users result history
            :param user_id: Users ID to update result value of
            :param value: Amount to update the account result by
            """
            user = self.get_user(user_id)
            user.result += value
            user.save()
            return user.result

        def update_funds(self, user_id, value):
            user = self.get_user(user_id)
            user.funds += value
            user.save()
            return user.funds
