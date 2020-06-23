from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.stock import *

router = DefaultRouter()
router.register(r'', StockViewSet, basename='stock')

urlpatterns = [
   path('<str:ticker>/favourite/', UserFavouriteStockView.as_view(), name='stock_favourite'),
   path('<str:ticker>/price/', StockPriceListView.as_view(), name='stock_price'),
   path('price/<int:pk>/', StockPriceRetrieveView.as_view(), name='price'),
]

urlpatterns += router.urls
