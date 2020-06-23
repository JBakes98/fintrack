from django.urls import path
from rest_framework.routers import DefaultRouter

from fintrack_be.views.user import *

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('login/', obtain_expiring_auth_token, name='get_token'),
    path('reset-password/', RequestUserPasswordReset.as_view(), name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='password_reset'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('get-email-verification/', UserRequestEmailVerificationAPIView.as_view(),
         name='request_email_verification'),
]

urlpatterns += router.urls
