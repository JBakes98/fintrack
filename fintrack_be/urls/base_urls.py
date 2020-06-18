from django.urls import path, include

urlpatterns = [
    path('stock/', include('fintrack_be.urls.stock_urls')),
    path('index/', include('fintrack_be.urls.index_urls')),
]
