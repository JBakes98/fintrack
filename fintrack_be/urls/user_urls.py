from django.urls import path
from fintrack_be.views.user import *

urlpatterns = [
    path('login/', obtain_expiring_auth_token, name='get_token'),
    path('retrieve/', UserDetailAPIView.as_view(), name='retrieve_user'),
    path('create/', UserCreateAPIView.as_view(), name='create_user'),
    path('update/', UserUpdateAPIView.as_view(), name='update_user'),
    path('delete/', UserDeleteAPIView.as_view(), name='delete_user'),

    path('reset-password/', RequestUserPasswordReset.as_view(), name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', UserPasswordResetView.as_view(), name='password_reset'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('get-email-verification/', UserRequestEmailVerificationAPIView.as_view(),
         name='request_email_verification'),

]
