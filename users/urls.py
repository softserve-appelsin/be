from django.urls import path

from .views import (CreateUserAPIView, GetAllUsersAPIView,
                    GetTokenForUserAPIView)

urlpatterns = [
    path("api/v1/create_user", CreateUserAPIView.as_view()),
    path("api/v1/get_all_users", GetAllUsersAPIView.as_view()),
    path("api/v1/token", GetTokenForUserAPIView.as_view()),
]
