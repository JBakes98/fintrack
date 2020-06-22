from django.urls import path
from rest_framework.routers import DefaultRouter

from industry.views import industry_views as views

router = DefaultRouter()
router.register(r'', views.IndustryViewSet, basename='industry')

urlpatterns = [
    path('companies/', views.IndustryCompanyListView.as_view()),
    path('<str:name>/companies/', views.IndustryCompanyRetrieveView.as_view()),
    # path('<str:name>/stocks/', views.IndustryStockListVIew.as_view()),
]

urlpatterns += router.urls
