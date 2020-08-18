from collections import OrderedDict
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.validators import validate_email
from django.db.models import EmailField
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_str

UserModel = get_user_model()


def email_address_exists(email):
    found = UserModel.objects.filter(email__iexact=email).exists()
    return found


def confirm_email(email_address):
    """
    Marks the email address as confirmed on the db
    """
    email_address.verified = True
    email_address.set_as_primary(conditional=True)
    email_address.save()


def send_confirmation_mail(request, signup, emailconfirmation):
    current_site = get_current_site(request)
    activate_url = get_current_site(request)
    ctx = {
        "user": emailconfirmation.email_address.user,
        "activate_url": activate_url,
        "current_site": current_site,
        "key": emailconfirmation.key,
    }
    if signup:
        email_template = 'email/email_confirmation_signup'
    else:
        email_template = 'email/email_confirmation'
    send_mail(email_template, emailconfirmation.email_address.email, ctx)


def cleanup_email_addresses(request, addresses):
    """
    Takes a list of EmailAddress instances and cleans it up, making
    sure only valid ones remain, without multiple primaries etc.

    Order is important: e.g. if multiple primary e-mail addresses
    exist, the first one encountered will be kept as primary.
    """
    from fintrack_be.models.email_address import EmailAddress
    # Let's group by `email`
    e2a = OrderedDict()  # maps email to EmailAddress
    primary_addresses = []
    verified_addresses = []
    primary_verified_addresses = []
    for address in addresses:
        # Pick up only valid ones...
        email = valid_email_or_none(address.email)
        if not email:
            continue
        # ... and non-conflicting ones...
        if EmailAddress.objects.filter(email__iexact=email).exists():
            continue
        a = e2a.get(email.lower())
        if a:
            a.primary = a.primary or address.primary
            a.verified = a.verified or address.verified
        else:
            a = address
            a.verified = a.verified
            e2a[email.lower()] = a
        if a.primary:
            primary_addresses.append(a)
            if a.verified:
                primary_verified_addresses.append(a)
        if a.verified:
            verified_addresses.append(a)
    # Now that we got things sorted out, let's assign a primary
    if primary_verified_addresses:
        primary_address = primary_verified_addresses[0]
    elif verified_addresses:
        # Pick any verified as primary
        primary_address = verified_addresses[0]
    elif primary_addresses:
        # Okay, let's pick primary then, even if unverified
        primary_address = primary_addresses[0]
    elif e2a:
        # Pick the first
        primary_address = e2a.keys()[0]
    else:
        # Empty
        primary_address = None
    # There can only be one primary
    for a in e2a.values():
        a.primary = primary_address.email.lower() == a.email.lower()
    return list(e2a.values()), primary_address


def valid_email_or_none(email):
    ret = None
    try:
        if email:
            validate_email(email)
            if len(email) <= EmailField().max_length:
                ret = email
    except ValidationError:
        pass
    return ret


def send_email_confirmation(request, user, signup=False):
    """
    E-mail verification mails are sent:
    a) Explicitly: when a user signs up
    b) Implicitly: when a user attempts to log in using an unverified
    e-mail while EMAIL_VERIFICATION is mandatory.

    Especially in case of b), we want to limit the number of mails
    sent (consider a user retrying a few times), which is why there is
    a cooldown period before sending a new mail. This cooldown period
    can be configured in ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN setting.
    """
    from fintrack_be.models.email_address import EmailAddress
    from fintrack_be.models.email_confirmation import EmailConfirmation

    cooldown_period = timedelta(seconds=settings.EMAIL_CONFIRMATION_COOLDOWN)

    email = user.email
    if email:
        try:
            email_address = EmailAddress.objects.get_for_user(user, email)
            if not email_address.verified:
                send_email = not EmailConfirmation.objects.filter(sent__gt=timezone.now() - cooldown_period,
                                                                  email_address=email_address).exists()
                if send_email:
                    email_address.send_confirmation(request, signup=signup)
            else:
                send_email = False
        except EmailAddress.DoesNotExist:
            send_email = True
            email_address = EmailAddress.objects.add_email(request,
                                                           user,
                                                           email,
                                                           signup=signup,
                                                           confirm=True)
            assert email_address
        # At this point, if we were supposed to send an email we have sent it.
        if send_email:
            add_message(
                request,
                messages.INFO,
                'account/messages/'
                'email_confirmation_sent.txt',
                {'email': email})


def add_message(request, level, message_template, message_context=None, extra_tags=''):
    """
    Wrapper of `django.contrib.messages.add_message`, that reads
    the message text from a template.
    """
    if 'django.contrib.messages' in settings.INSTALLED_APPS:
        try:
            if message_context is None:
                message_context = {}
            message = render_to_string(message_template,
                                       message_context).strip()
            if message:
                messages.add_message(request, level, message,
                                     extra_tags=extra_tags)
        except TemplateDoesNotExist:
            pass


def send_mail(template_prefix, email, context):
    msg = render_mail(template_prefix, email, context)
    msg.send()


def render_mail(template_prefix, email, context):
    """
    Renders an e-mail to `email`.  `template_prefix` identifies the
    e-mail that is to be sent, e.g. "email/email_confirmation"
    """
    subject = render_to_string('{0}_subject.txt'.format(template_prefix), context)
    # remove superfluous line breaks
    subject = " ".join(subject.splitlines()).strip()
    subject = format_email_subject(subject)

    bodies = {}
    for ext in ['html', 'txt']:
        try:
            template_name = '{0}_message.{1}'.format(template_prefix, ext)
            bodies[ext] = render_to_string(template_name, context).strip()
        except TemplateDoesNotExist:
            if ext == 'txt' and not bodies:
                # We need at least one body
                raise
    if 'txt' in bodies:
        msg = EmailMultiAlternatives(subject, bodies['txt'], [email])
        if 'html' in bodies:
            msg.attach_alternative(bodies['html'], 'text/html')
    else:
        msg = EmailMessage(subject, bodies['html'], [email])
        msg.content_subtype = 'html'  # Main content is now text/html
    return msg


def format_email_subject(subject):
    prefix = 'Fintrack'
    if prefix is None:
        site = get_current_site(self.request)
        prefix = "[{name}] ".format(name=site.name)
    return prefix + force_str(subject)
