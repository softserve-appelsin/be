from django.urls import path, include
from .views import CreateUserAPIView, GetAllUsersAPIView, GetTokenForUserAPIView, UserProfileTypesAPIView, UserInfoAPIView, LogoutAPIView, RefreshTokenAPIView

urlpatterns = [
    path('create_user/', CreateUserAPIView.as_view()),
    path('get_all_users/', GetAllUsersAPIView.as_view()),
    path('token/', GetTokenForUserAPIView.as_view()),
    path('profile_types/', UserProfileTypesAPIView.as_view()),
    path('user_info/<str:username>/', UserInfoAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh_token/', RefreshTokenAPIView.as_view())

]
