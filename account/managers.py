from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
        if not password:
            raise ValueError('Password must be provided')

        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def find_by_email(self, email):
        queryset = self.get_queryset()
        return queryset.filter(email=email)

    def factory_user_account(self, email, password, **kwargs):
        # Factory to create a user account
        return self.create_user(email, password, **kwargs)
