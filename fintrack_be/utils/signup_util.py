from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

from fintrack_be.utils import email_util


def perform_login(request, user, signup=False):
    """
    signup -- Indicates whether or not sending the
    email is essential (during signup).
    """
    if not user.is_active:
        return HttpResponseRedirect(reverse('account_inactive'))

    from fintrack_be.models.email_address import EmailAddress
    has_verified_email = EmailAddress.objects.filter(user=user, verified=True).exists()

    if not has_verified_email:
        email_util.send_email_confirmation(request, user, signup=signup)
        return HttpResponseRedirect(reverse('account_email_verification_sent'))

    authenticate(request)
    response = 'logged in'
    email_util.add_message(request, messages.SUCCESS, 'account/messages/logged_in.txt', {'user': user})

    return response


def complete_signup(request, user):
    return perform_login(request, user, signup=True)
