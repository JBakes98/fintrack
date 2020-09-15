from django.urls import path
from rest_framework.routers import DefaultRouter

from exchange.views import *

router = DefaultRouter()
router.register(r'', ExchangeViewSet, basename='exchanges')

urlpatterns = [
    path('stocks/', ExchangeStockListView.as_view(), name='exchanges_stocks'),
    path('<str:symbol>/stocks/', ExchangeStockRetrieveView.as_view(), name='exchange_stocks'),
]

urlpatterns += router.urls
