from django.urls import path
from rest_framework.routers import DefaultRouter

from exchange.views import exchange_views as views

router = DefaultRouter()
router.register(r'', views.ExchangeViewSet, basename='exchange')

urlpatterns = [
    path('stocks/', views.ExchangeStockListView.as_view()),
    path('<str:symbol>/stocks/', views.ExchangeStockRetrieveView.as_view()),
]

urlpatterns += router.urls
