from django.urls import path
from stock.views import stock_views

urlpatterns = [
   path('list/', stock_views.StockListView.as_view()),
   path('<str:ticker>/', stock_views.StockDetailView.as_view()),
   path('<str:ticker>/favourite/', stock_views.UserFavouriteStockView.as_view()),
   path('<str:ticker>/price-data/', stock_views.StockPriceListView.as_view()),
   path('all-price-data/', stock_views.AllStockPriceDataListView.as_view()),
]
