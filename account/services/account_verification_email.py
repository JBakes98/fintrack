from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import User
from account.utils import email_util


class AccountVerificationEmail:
    def __init__(self, to_email):
        self.subject_template_name = 'account_verification_subject.txt'
        self.email_template_name = 'account_verification_email.html'
        self.use_https = False
        self.token_generator = default_token_generator
        self.from_email = None
        self._to_email = to_email
        self.request = None
        self.html_email_template_name = None
        self.extra_email_context = None

    def send(self):
        """
            Generate a one-use only link for verifying user account and send
            it to the user email.
            """
        user = User.objects.get(email=self._to_email)

        site_name = domain = settings.DEFAULT_DOMAIN

        # Build the context data for the email
        context = {
            'email': self._to_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': self.token_generator.make_token(user),
            'protocol': 'https' if self.use_https else 'http',
            **(self.extra_email_context or {}),
        }

        email_util.send_mail(
            self.subject_template_name, self.email_template_name, context, self.from_email,
            self._to_email, html_email_template_name=self.html_email_template_name,
        )