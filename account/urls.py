from django.urls import path
from account.views import AddStreamerView, AdminLoginView, SendPasswordResetEmailView, StreamerLoginView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView, LogoutAllView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/user/', UserLoginView.as_view(), name='login'),
    path('login/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('addstreamer/', AddStreamerView.as_view(), name='AddStreamer'),
    path('login/admin/',AdminLoginView.as_view(),name='AdminLogin'),
    path('login/streamer/',StreamerLoginView.as_view(),name='StreamerLogin'),
    # path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),


]
