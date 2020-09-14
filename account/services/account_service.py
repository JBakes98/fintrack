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

    @staticmethod
    def send_verification_email(domain_override=None,
                                subject_template_name='account_verification_subject.txt',
                                email_template_name='account_verification_email.html',
                                use_https=False, token_generator=default_token_generator,
                                from_email=None, to_email=None, request=None,
                                html_email_template_name=None, extra_email_context=None):
        """
        Generate a one-use only link for verifying user account and send
        it to the user email.
        """
        email_field_name = UserModel.get_email_field_name()
        user = UserModel.objects.get(email=to_email)
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        user_email = getattr(user, email_field_name)
        context = {
            'email': user_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        email_util.send_mail(
            subject_template_name, email_template_name, context, from_email,
            user_email, html_email_template_name=html_email_template_name,
        )
