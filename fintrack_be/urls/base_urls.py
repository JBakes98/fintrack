from django.urls import path, include

urlpatterns = [
    # path('country/', include('fintrack_be.urls.country_urls')),
    path('company/', include('fintrack_be.urls.company_urls')),
    path('stock/', include('fintrack_be.urls.stock_urls')),
    path('index/', include('fintrack_be.urls.index_urls')),
]
