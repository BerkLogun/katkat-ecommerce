from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    user_profile, 
    update_profile
)

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user_register'),
    path('register/', UserRegistrationView.as_view(), name='user_register_slash'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('login/', UserLoginView.as_view(), name='user_login_slash'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh_slash'),
    path('profile', user_profile, name='user_profile'),
    path('profile/', user_profile, name='user_profile_slash'),
    path('profile/update', update_profile, name='update_profile'),
    path('profile/update/', update_profile, name='update_profile_slash'),
] 