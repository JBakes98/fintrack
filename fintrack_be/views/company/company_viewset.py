from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import Company
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing Companies or Retrieve specific Company


    The User must be a Verified Admin User to use this methods
    POST - Create new Company
    PUT - Fully update existing Company
    PATCH - Partially update existing Company
    DELETE - Delete existing Company
    """
    serializer_class = CompanySerializer
    lookup_field = 'short_name'
    lookup_value_regex = '[^/]+'

    def get_queryset(self):
        return Company.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
