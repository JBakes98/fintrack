from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('console/', admin.site.urls),
    path('', include('fintrack_fe.urls')),
    path('api/v1/user/', include('fintrack_be.urls.user_urls')),
    path('api/v1/country/', include('fintrack_be.urls.country_urls')),
    path('api/v1/sector/', include('fintrack_be.urls.sector_urls')),
    path('api/v1/industry/', include('fintrack_be.urls.industry_urls')),
    path('api/v1/exchange/', include('fintrack_be.urls.exchange_urls')),
    path('api/v1/company/', include('fintrack_be.urls.company_urls')),
    path('api/v1/stock/', include('fintrack_be.urls.stock_urls')),
    path('api/v1/index/', include('fintrack_be.urls.index_urls')),
    path('api/v1/position/', include('fintrack_be.urls.position_urls'))
]
