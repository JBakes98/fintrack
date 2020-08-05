from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

UserModel = get_user_model()


def email_address_exists(email):
    found = UserModel.objects.filter(email__iexact=email).exists()
    return found


def confirm_email(self, request, email_address):
    """
    Marks the email address as confirmed on the db
    """
    email_address.verified = True
    email_address.set_as_primary(conditional=True)
    email_address.save()


def send_confirmation_mail(self, request, emailconfirmation, signup):
    current_site = get_current_site(request)
    activate_url = self.get_email_confirmation_url(
        request,
        emailconfirmation)
    ctx = {
        "user": emailconfirmation.email_address.user,
        "activate_url": activate_url,
        "current_site": current_site,
        "key": emailconfirmation.key,
    }
    if signup:
        email_template = 'account/email/email_confirmation_signup'
    else:
        email_template = 'account/email/email_confirmation'
    self.send_mail(email_template,
                   emailconfirmation.email_address.email,
                   ctx)
