from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

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
    return UserModel.objects.filter(email=email)


def send_verification_email(domain_override=None,
                            subject_template_name='account_verification_subject.txt',
                            email_template_name='account_verification_email.html',
                            use_https=False, token_generator=default_token_generator,
                            from_email=None, to_email=None, request=None,
                            html_email_template_name=None, extra_email_context=None):
    """
    Generate a one-use only link for verifying user account and send
    it to the user email.
    """
    email = to_email
    email_field_name = UserModel.get_email_field_name()
    for user in get_users(email):
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        user_email = getattr(user, email_field_name)
        context = {
            'email': user_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        send_mail(
            subject_template_name, email_template_name, context, from_email,
            user_email, html_email_template_name=html_email_template_name,
        )
