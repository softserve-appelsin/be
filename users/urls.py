from django.contrib import admin
from django.urls import path, include
from .views import CreateUserAPIView, GetAllUsersAPIView, GetTokenForUserAPIView, UserProfileTypesAPIView, UserFullNameAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/create_user', CreateUserAPIView.as_view()),
    path('api/v1/get_all_users', GetAllUsersAPIView.as_view()),
    path('api/v1/token', GetTokenForUserAPIView.as_view()),
    path('api/v1/profile_types', UserProfileTypesAPIView.as_view()),
    path('api/v1/user_full_name', UserFullNameAPIView.as_view())

]
