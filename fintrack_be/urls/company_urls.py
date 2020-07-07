from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.company import *

router = DefaultRouter()
router.register(r'', CompanyViewSet, basename='company')

urlpatterns = [
   path('<str:name>/shares/', CompanySharesListView.as_view(), name='company_shares'),
]

urlpatterns += router.urls
