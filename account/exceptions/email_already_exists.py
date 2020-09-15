from rest_framework.exceptions import APIException


class EmailAlreadyExistsError(APIException):
    pass

