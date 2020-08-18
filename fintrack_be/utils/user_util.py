from django.contrib.auth import get_user_model
from fintrack_be.utils import email_util


def new_user(request):
    """
    Instantiates a new User instance.
    """
    user = get_user_model()()
    return user


def save_user(request, user, form, commit=True):
    """
    Saves a new `User` instance using information provided
    """
    data = form.cleaned_data
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    if 'password1' in data:
        user.set_password(data["password1"])
    else:
        user.set_unusable_password()
    if commit:
        print(user)
        user.save()
    return user


def setup_user_email(request, user, addresses):
    """
    Creates proper EmailAddress for the user that was just signed
    up. Only sets up, doesn't do any other handling such as sending
    out email confirmation mails etc.
    """
    from fintrack_be.models.email_address import EmailAddress

    assert not EmailAddress.objects.filter(user=user).exists()
    priority_addresses = []
    email = user.email
    if email:
        priority_addresses.append(EmailAddress(user=user, email=email, primary=True, verified=False))
    addresses, primary = email_util.cleanup_email_addresses(request, priority_addresses + addresses)
    for a in addresses:
        a.user = user
        a.save()
    EmailAddress.objects.fill_cache_for_user(user, addresses)
    if (primary and email and email.lower() != primary.email.lower()):
        user.email
        user.save()
    return primary