from django.urls import path
from rest_framework.routers import DefaultRouter

from stock.views import *

router = DefaultRouter()
router.register(r'', StockViewSet, basename='stocks')

urlpatterns = [
   path('watchlist/<str:ticker>/', WatchStockView.as_view(), name='watchlist_stock'),
   path('watchlist/', UserWatchlistAPIView.as_view(), name='stock_watchlist'),
   path('<str:ticker>/price/', StockPriceListView.as_view(), name='stock_price'),
   path('price/<int:pk>/', StockPriceRetrieveView.as_view(), name='price'),
   path('correlations/', StocksCorrelation.as_view(), name='stock_correlations'),
]

urlpatterns += router.urls
