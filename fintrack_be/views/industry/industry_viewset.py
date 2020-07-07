from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from fintrack_be.models import Industry
from fintrack_be.serializers import IndustrySerializer
from fintrack_be.permissions import IsVerified


class IndustryViewSet(viewsets.ModelViewSet):
    """
        Industry ViewSet that offers the following actions, list(), retrieve(),
        create(), update(), partial_update() and destroy(). Depending on the
        HTTP method the User will require different permissions.

        The User must be Verified to use this method
        GET - List existing Industries or Retrieve specific Industry


        The User must be a Verified Admin User to use this methods
        POST - Create new Industry
        PUT - Fully update existing Industry
        PATCH - Partially update existing Industry
        DELETE - Delete existing Industry

        """
    serializer_class = IndustrySerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Industry.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())

    def list(self, request, *args, **kwargs):
        query_params = {'sector__name': self.request.query_params.get('sector', None)}
        arguments = {}

        for k, v in query_params.items():
            if v:
                arguments[k] = v

        queryset = Industry.objects.filter(**arguments).order_by('name')
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
