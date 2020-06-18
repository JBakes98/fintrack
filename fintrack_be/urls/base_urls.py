from django.urls import path, include

urlpatterns = [
    path('index/', include('fintrack_be.urls.index_urls')),
]
