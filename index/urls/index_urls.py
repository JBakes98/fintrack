from django.urls import path
from rest_framework.routers import DefaultRouter

from index.views import index_views as views

router = DefaultRouter()
router.register(r'', views.IndexViewSet, basename='index')

urlpatterns = [
   path('<str:symbol>/correlation/', views.IndexCorrelationAPIView.as_view()),
]

urlpatterns += router.urls
