from django.contrib import admin
from django.urls import path, include
from fintrack import views

urlpatterns = [
    path('', views.index),
    path('console/', admin.site.urls),

    path('api/v1/user/', include('user.urls')),
    path('api/v1/country/', include('country.urls')),
    path('api/v1/sector/', include('sector.urls')),
    path('api/v1/industry/', include('industry.urls')),
    path('api/v1/exchange/', include('exchange.urls')),
    path('api/v1/company/', include('company.urls')),
    path('api/v1/stock/', include('stock.urls')),
    path('api/v1/index/', include('index.urls')),
]
