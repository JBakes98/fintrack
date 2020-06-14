from django.urls import path

from fintrack_be.views import index_views

urlpatterns = [
   path('list/', index_views.IndexListView.as_view()),
   path('<str:symbol>/correlation/', index_views.IndexCorrelationAPIView.as_view()),
]