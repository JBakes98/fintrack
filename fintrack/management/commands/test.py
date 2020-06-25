from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from fintrack_be.helpers import user_token
from fintrack_be.models import EmailList, EmailTemplate, User
from fintrack_be.serializers import UserSerializer
from fintrack_be.tasks import send_email


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(email='joshbaker286.jb@gmail.com')

        send_email.delay('account-authentication',
                         emails=[user.email, ],
                         context={
                             'domain': '192.168.1.97:1111',
                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                             'token': user_token.make_token(user),
                             'user': UserSerializer(user).data
                         }
                         )

