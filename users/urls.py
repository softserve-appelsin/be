from django.contrib import admin
from django.urls import path, include
from .views import CreateUserAPIView, GetAllUsersAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/v1/auth/token', TokenObtainPairView.as_view()),
    path('api/v1/auth/refresh', TokenRefreshView.as_view()),
    path('api/v1/create_user', CreateUserAPIView.as_view()),
    path('api/v1/get_all_users', GetAllUsersAPIView.as_view())
]
