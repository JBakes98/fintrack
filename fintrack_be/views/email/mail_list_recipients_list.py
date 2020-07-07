from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from fintrack_be.models import MailList
from fintrack_be.serializers.email.mail_list_serializer import MailListRecipientsSerializer


class MailListRecipientsRetrieveView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = MailListRecipientsSerializer

    def get_object(self):
        name = self.kwargs['name']
        return get_object_or_404(MailList, name=name)
