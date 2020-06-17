from django.urls import path
from user.views import user_views as views

urlpatterns = [
    path('login/', views.obtain_expiring_auth_token, name='get_token'),
    path('retrieve/', views.UserDetailAPIView.as_view(), name='retrieve_user'),
    path('create/', views.UserCreateAPIView.as_view(), name='create_user'),
    path('update/', views.UserUpdateAPIView.as_view(), name='update_user'),
    path('delete/', views.UserDeleteAPIView.as_view(), name='delete_user'),

    path('reset-password/', views.RequestUserPasswordReset.as_view(), name='request_password_reset'),
    path('reset-password/<uidb64>/<token>/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    path('get-email-verification/', views.UserRequestEmailVerificationAPIView.as_view(),
         name='request_email_verification'),

]
