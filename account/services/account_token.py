import datetime
from rest_framework.authtoken.models import Token
from account.models import User


class AccountToken:
    def __init__(self, id, email):
        self._id = id
        self._email = email

    def create_user_token(self):
        """
        Function used to create a users auth token when signing in.
        :param user_id: User Id to create their auth token
        :return: The users auth token
        """
        user = User.objects.get(**self.__dict__)
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()
        return token