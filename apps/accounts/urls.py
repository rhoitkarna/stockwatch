from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView,
    RegisterView,
    UserProfileView,
    LogoutView,
    ChangePasswordView,
)

urlpatterns = [
    # Auth Endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # User Profile / Management
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change_password'),
]