from django.urls import path
from rest_framework.routers import DefaultRouter

from company.views import company_views as views

router = DefaultRouter()
router.register(r'', views.CompanyViewSet, basename='company')

urlpatterns = [
   path('<str:name>/shares/', views.CompanySharesListView.as_view()),
]

urlpatterns += router.urls
