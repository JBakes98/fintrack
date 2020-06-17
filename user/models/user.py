import uuid
import pytz

import django
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.models.user_account_manager import UserAccountManager
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

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserAccountManager()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


@receiver(django.db.models.signals.post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    from rest_framework.authtoken.models import Token
    import datetime

    if created:
        if instance.is_active:
            token, created = Token.objects.get_or_create(user=instance)
            if not created:
                token.delete()
                token = Token.objects.create(user=instance)
                token.created = datetime.datetime.utcnow()
                token.save()
