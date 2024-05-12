from django.urls import path, include
from .views import CreateUserAPIView, GetTokenForUserAPIView, LogoutAPIView, RefreshTokenAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view(), name='create-user'),
    path('token/', GetTokenForUserAPIView.as_view(), name='login-user'),
    path('logout/', LogoutAPIView.as_view(), name='logout-user'),
    path('refresh_token/', RefreshTokenAPIView.as_view(), name='refresh-token')
]
