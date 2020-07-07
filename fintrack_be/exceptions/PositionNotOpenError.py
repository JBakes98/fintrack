from rest_framework import exceptions, status


class PositionNotOpenError(exceptions.APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Position already closed"
