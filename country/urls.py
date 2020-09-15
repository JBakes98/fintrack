from django.urls import path
from rest_framework.routers import DefaultRouter

from country.views import *

router = DefaultRouter()
router.register(r'', CountryViewSet, basename='countries')

urlpatterns = [
    path('exchanges/', CountryExchangeListView.as_view(), name='countries_exchanges'),
    path('<str:alpha2>/exchanges/', CountryExchangeRetrieveView.as_view(), name='country_exchanges'),
]

urlpatterns += router.urls
