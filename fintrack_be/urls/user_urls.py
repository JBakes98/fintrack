from django.urls import path, re_path

from fintrack_be.views.user import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('detail/', UserDetailsView.as_view(), name='rest_user_detail'),

    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    re_path(r'^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{'
            r'1,20})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('watchlist/', WatchlistAPIView.as_view(), name='user_watchlist'),

]
