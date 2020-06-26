from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import MailList
from fintrack_be.permissions import IsVerified
from fintrack_be.serializers.email.mail_list_serializer import MailListSerializer


class MailListViewSet(viewsets.ModelViewSet):
    """
    EmailList ViewSet that offers the following actions, list(), retrieve(),
    create(), update(), partial_update() and destroy(). Depending on the
    HTTP method the User will require different permissions.

    The User must be Verified to use this method
    GET - List existing EmailLists or Retrieve specific EmailList


    The User must be a Verified Admin User to use this methods
    POST - Create new EmailList
    PUT - Fully update existing EmailList
    PATCH - Partially update existing EmailList
    DELETE - Delete existing EmailList
    """
    serializer_class = MailListSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return MailList.objects.all()

    def get_permissions(self):
        request_method = self.request.method
        if request_method == 'GET':
            return (IsAuthenticated(), IsVerified())
        else:
            return (IsAdminUser(), IsVerified())
