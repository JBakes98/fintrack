from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.exchange import *

router = DefaultRouter()
router.register(r'', ExchangeViewSet, basename='exchange')

urlpatterns = [
    path('stocks/', ExchangeStockListView.as_view(), name='exchanges_stocks'),
    path('<str:symbol>/stocks/', ExchangeStockRetrieveView.as_view(), name='exchange_stocks'),
]

urlpatterns += router.urls
