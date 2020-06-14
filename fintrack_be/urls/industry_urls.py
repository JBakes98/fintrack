from django.urls import path
from fintrack_be.views import industry_views

urlpatterns = [
    path('list/', industry_views.IndustryListView.as_view()),
    path('<str:name>/', industry_views.IndustryDetailView.as_view()),
    path('<str:name>/companies/', industry_views.IndustryCompanyListView.as_view()),
    path('<str:name>/stocks/', industry_views.IndustryStockListVIew.as_view()),
]
