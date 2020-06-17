from django.urls import path

from country import views

urlpatterns = [
    path('list/', views.CountryListView.as_view()),
]
