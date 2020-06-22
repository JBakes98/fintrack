from django.urls import path
from rest_framework.routers import DefaultRouter

from country import views

router = DefaultRouter()
router.register(r'', views.CountryViewSet, basename='country')

urlpatterns = [
    path('exchanges/', views.CountryExchangeListView.as_view()),
    path('<str:alpha2>/exchanges/', views.CountryExchangeRetrieveView.as_view()),
]

urlpatterns += router.urls
