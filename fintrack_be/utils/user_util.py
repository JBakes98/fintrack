from django.contrib.auth import get_user_model
from fintrack_be.utils import email_util


def new_user():
    """
    Instantiates a new User instance.
    """
    user = get_user_model()()
    return user


def save_user(user, data):
    """
    Saves a new `User` instance using information provided
    """
    data = form.cleaned_data
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')

    ###
    # This is a temporary solution until user verification is implemented this should never be used in
    # production deployements
    user.verified = True
    ###

    if 'password1' in data:
        user.set_password(data["password1"])
    else:
        user.set_unusable_password()
    user.save()
    return user
