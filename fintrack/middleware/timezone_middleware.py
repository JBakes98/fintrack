import pytz
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        timezone.activate(pytz.timezone(getattr(user, 'timezone', 'UTC')))
        return self.get_response(request)
