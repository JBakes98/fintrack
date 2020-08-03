from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.management.base import BaseCommand
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from fintrack_be.helpers import user_token
from fintrack_be.models import MailList, EmailTemplate, User, Exchange, Index
from fintrack_be.serializers import UserSerializer
from fintrack_be.tasks import send_email, send_mail_list


class Command(BaseCommand):

    def handle(self, *args, **options):
        for e in Index.objects.with_stock_count():
            print(e.num_stocks)