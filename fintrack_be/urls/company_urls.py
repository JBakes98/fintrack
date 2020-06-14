from django.urls import path
from fintrack_be.views import company_views

urlpatterns = [
   path('list/', company_views.CompanyListView.as_view()),
   path('<str:name>/', company_views.CompanyDetailView.as_view()),
   path('<str:name>/shares/', company_views.CompanySharesListView.as_view()),
]
