from django.urls import path, re_path

from account.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('detail/', UserDetailsView.as_view(), name='user_detail'),
    re_path(r'^account/verification/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{'
            r'1,20})/$', AccountVerifyConfirmView.as_view(), name='account_verify_confirm'),

    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{'
            r'1,20})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
