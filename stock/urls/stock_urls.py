from django.urls import path
from rest_framework.routers import DefaultRouter

from stock.views import stock_views as views

router = DefaultRouter()
router.register(r'', views.StockViewSet, basename='stock')

urlpatterns = [
   path('<str:ticker>/favourite/', views.UserFavouriteStockView.as_view()),
   path('<str:ticker>/price/', views.StockPriceListView.as_view()),
   path('price/<int:pk>/', views.PriceRetrieveView.as_view()),
]

urlpatterns += router.urls
