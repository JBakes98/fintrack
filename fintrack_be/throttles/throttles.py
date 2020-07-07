from rest_framework.throttling import UserRateThrottle


class OncePerHourUserThrottle(UserRateThrottle):
    rate = '1/hour'
