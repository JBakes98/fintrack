from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.position import PositionViewSet

router = DefaultRouter()
router.register(r'', PositionViewSet, basename='position')
urlpatterns = router.urls
