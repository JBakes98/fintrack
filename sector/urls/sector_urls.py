from django.urls import path
from sector import views

urlpatterns = [
   path('list/', views.SectorListCreateView.as_view()),
   path('<str:name>/', views.SectorDetailView.as_view()),
   path('<str:name>/companies/', views.SectorCompanyListView.as_view()),
   path('<str:name>/stocks/', views.SectorStockListView.as_view()),
]
