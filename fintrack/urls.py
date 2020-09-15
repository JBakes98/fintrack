from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('console/', admin.site.urls),
    path('', include('fintrack_fe.urls')),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/countries/', include('country.urls')),
    path('api/v1/sectors/', include('sector.urls')),
    path('api/v1/industries/', include('industry.urls')),
    path('api/v1/exchanges/', include('exchange.urls')),
    path('api/v1/companies/', include('company.urls')),
    path('api/v1/stocks/', include('stock.urls')),
]
