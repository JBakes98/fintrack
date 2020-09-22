from django.urls import path
from rest_framework.routers import DefaultRouter

from index.views import *

router = DefaultRouter()
router.register(r'', IndexViewSet, basename='indices')

urlpatterns = [
   path('<str:symbol>/correlation/', IndexCorrelationListView.as_view(), name='index_correlations'),
]

urlpatterns += router.urls
