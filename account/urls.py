from django.urls import path, re_path

from account.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('detail/', UserDetailsView.as_view(), name='user_detail'),
    path('verification/confirm/<str:uidb64>/<str:token>/', AccountVerifyConfirmView.as_view(), name='account_verify_confirm'),

    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
