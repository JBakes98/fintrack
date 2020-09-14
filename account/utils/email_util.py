from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

UserModel = get_user_model()


def email_address_exists(email):
    """
    Checks if a specific email address already exists against a user account
    """
    found = UserModel.objects.filter(email__iexact=email).exists()
    return found


def confirm_email(email_address):
    """
    Marks the email address as confirmed on the db
    """
    email_address.verified = True
    email_address.save()

