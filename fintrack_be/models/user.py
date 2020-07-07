import datetime
import uuid
import pytz
import decimal

import django
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.authtoken.models import Token

from fintrack_be.helpers import user_token
from fintrack_be.models.user_account_manager import UserAccountManager
from fintrack_be.models.country import Country
from fintrack_be.models.stock import Stock


class User(AbstractBaseUser, PermissionsMixin):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    verified = models.DateTimeField(default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    last_login = models.DateTimeField(default=django.utils.timezone.now)
    timezone = models.CharField(max_length=50, default='UTC', choices=TIMEZONES, null=False, blank=False)

    favourite_stocks = models.ManyToManyField(Stock, related_name='favourite_stock')
    funds = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)
    value = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)
    result = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserAccountManager()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def update_funds(self, value):
        print(value)
        self.funds += value
        self.save()
        return self.funds

    def sufficient_funds(self, value):
        return self.funds >= value

    def update_result(self, value):
        self.result += value
        self.save()
        return self.result

    def create_user_token(self):
        token, created = Token.objects.get_or_create(user=self)
        if not created:
            token.delete()
            token = Token.objects.create(user=self)
            token.created = datetime.datetime.utcnow()
            token.save()

    def send_verification_email(self):
        from fintrack_be.serializers.user.user_serializer import UserSerializer
        from fintrack_be.tasks.email.email_tasks import send_email

        current_site = get_current_site(self.request)
        send_email.delay('account-verification',
                         emails=[self.email, ],
                         context={
                             'domain': current_site.domain,
                             'uid': urlsafe_base64_encode(force_bytes(self.pk)),
                             'token': user_token.make_token(self),
                             'user': UserSerializer(self).data
                         }
                         )

