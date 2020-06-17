from django.urls import path, include

urlpatterns = [
    # path('country/', include('fintrack_be.urls.country_urls')),
    path('company/', include('fintrack_be.urls.company_urls')),
    path('exchange/', include('fintrack_be.urls.exchange_urls')),
    path('sector/', include('fintrack_be.urls.sector_urls')),
    path('industry/', include('fintrack_be.urls.industry_urls')),
    path('stock/', include('fintrack_be.urls.stock_urls')),
    path('index/', include('fintrack_be.urls.index_urls')),
]
