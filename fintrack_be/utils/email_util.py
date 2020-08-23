from django.contrib.auth import get_user_model

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


"""
Below is a draft of what the user email verification methodology would look like, I am not implementing this at the
moment as I wish to focus on core functionality of the site first
"""
# def send_confirmation_mail(request, signup, emailconfirmation):
#     current_site = get_current_site(request)
#     activate_url = get_current_site(request)
#     ctx = {
#         "user": emailconfirmation.email_address.user,
#         "activate_url": activate_url,
#         "current_site": current_site,
#         "key": emailconfirmation.key,
#     }
#     if signup:
#         email_template = 'email/email_confirmation_signup'
#     else:
#         email_template = 'email/email_confirmation'
#     send_mail(email_template, emailconfirmation.email_address.email, ctx)

