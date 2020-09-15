from django.urls import path
from rest_framework.routers import DefaultRouter

from company.views import *

router = DefaultRouter()
router.register(r'', CompanyViewSet, basename='companies')

urlpatterns = [
   path('<str:name>/shares/', CompanySharesListView.as_view(), name='company_shares'),
]

urlpatterns += router.urls
