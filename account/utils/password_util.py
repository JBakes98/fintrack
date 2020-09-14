from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.forms import forms
from django.utils.translation import gettext_lazy as _


def clean_password(password, user=None):
    """
    Validates a password. You can hook into this if you want to
    restric the allowed password choices.
    """
    min_length = settings.PASSWORD_MIN_LENGTH
    if min_length and len(password) < min_length:
        raise forms.ValidationError(_("Password must be a minimum of {0} "
                                      "characters.").format(min_length))
    validate_password(password, user)
    return password
