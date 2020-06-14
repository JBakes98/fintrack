from django.urls import path
from fintrack_be.views import sector_views


urlpatterns = [
   path('list/', sector_views.SectorListView.as_view()),
   path('<str:name>/', sector_views.SectorDetailView.as_view()),
   path('<str:name>/companies/', sector_views.SectorCompanyListView.as_view()),
   path('<str:name>/stocks/', sector_views.SectorStockListView.as_view()),
]
