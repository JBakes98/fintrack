from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.index import *

router = DefaultRouter()
router.register(r'', IndexViewSet, basename='index')

urlpatterns = [
   path('<str:symbol>/correlation/', IndexCorrelationListView.as_view(), name='index_correlations'),
]

urlpatterns += router.urls
