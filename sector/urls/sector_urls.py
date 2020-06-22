from django.urls import path
from rest_framework.routers import DefaultRouter

from sector import views

router = DefaultRouter()
router.register(r'', views.SectorViewSet, basename='sector')

urlpatterns = [
   path('<str:name>/industries/', views.SectorIndustryListView.as_view()),
   path('<str:name>/companies/', views.SectorCompanyListView.as_view()),
   path('<str:name>/stocks/', views.SectorStockListView.as_view()),
]

urlpatterns += router.urls