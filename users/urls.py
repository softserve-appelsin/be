from django.contrib import admin
from django.urls import path, include
from .views import CreateUserAPIView, GetAllUsersAPIView, GetTokenForUserAPIView, UserProfileTypesAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view()),
    path('get_all_users/', GetAllUsersAPIView.as_view()),
    path('token/', GetTokenForUserAPIView.as_view()),
    path('profile_types/', UserProfileTypesAPIView.as_view()),
]
