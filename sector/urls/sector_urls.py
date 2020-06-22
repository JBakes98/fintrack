from django.urls import path
from rest_framework.routers import DefaultRouter

from sector import views

router = DefaultRouter()
router.register(r'', views.SectorViewSet, basename='sector')

urlpatterns = [
   path('industries/', views.SectorIndustryListView.as_view(), name='sectors-industries'),
   path('<str:name>/industries/', views.SectorIndustryRetrieveView.as_view(), name='sector-industries'),
   # path('<str:name>/companies/', views.SectorCompanyListView.as_view(), name='sector-companies'),
   # path('<str:name>/stocks/', views.SectorStockListView.as_view()),
]

urlpatterns += router.urls