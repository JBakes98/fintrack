from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.email import *

router = DefaultRouter()
router.register(r'', MailListViewSet, basename='mail-list')

urlpatterns = [
    path('<str:name>/recipients/', MailListRecipientsRetrieveView.as_view(), name='mail_list_recipients'),
]

urlpatterns += router.urls
