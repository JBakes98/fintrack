from django.urls import path
from company.views import company_views as views


urlpatterns = [

   path('list/', views.CompanyListCreateView.as_view()),
   path('<str:name>/', views.CompanyRetrieveUpdateDestroyView.as_view()),
   path('<str:name>/shares/', views.CompanySharesListView.as_view()),
]
