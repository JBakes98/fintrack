from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template import loader


UserModel = get_user_model()


def email_address_exists(email):
    """
    Checks if a specific email address already exists against a user account
    """
    found = UserModel.objects.filter(email__iexact=email).exists()
    return found


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


def get_users(email):
    """
    Function to return users with an email
    """
    return UserModel.objects.filter(email=email)


