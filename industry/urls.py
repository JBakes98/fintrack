from django.urls import path
from rest_framework.routers import DefaultRouter

from industry.views import *

router = DefaultRouter()
router.register(r'', IndustryViewSet, basename='industries')

urlpatterns = [
    path('companies/', IndustryCompanyListView.as_view(), name='industries_companies'),
    path('<str:name>/companies/', IndustryCompanyRetrieveView.as_view(), name='industry_companies'),
    path('<str:name>/stocks/', IndustryStockListVIew.as_view(), name='industry_stocks'),
]

urlpatterns += router.urls
