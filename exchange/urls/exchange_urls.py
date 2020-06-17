from django.urls import path
from exchange.views import exchange_views

urlpatterns = [
   path('list/', exchange_views.ExchangeListView.as_view()),
   path('<str:symbol>/', exchange_views.ExchangeDetailView.as_view()),
   path('<str:symbol>/constituents/', exchange_views.ExchangeStocksList.as_view()),
]
