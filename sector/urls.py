from django.urls import path
from rest_framework.routers import DefaultRouter

from sector.views import *

router = DefaultRouter()
router.register(r'', SectorViewSet, basename='sector')

urlpatterns = [
   path('industries/', SectorIndustryListView.as_view(), name='sectors-industries'),
   path('<str:name>/industries/', SectorIndustryRetrieveView.as_view(), name='sector-industries'),
   # path('<str:name>/companies/', SectorCompanyListView.as_view(), name='sector-companies'),
   # path('<str:name>/stocks/', SectorStockListView.as_view()),
]

urlpatterns += router.urls
