from django.urls import path, include
from .views import CreateUserAPIView, GetTokenForUserAPIView, LogoutAPIView, RefreshTokenAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view()),
    path('token/', GetTokenForUserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh_token/', RefreshTokenAPIView.as_view())
]
