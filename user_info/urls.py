from django.urls import path
from .views import GetAllUsersAPIView, UserProfileTypesAPIView, UserInfoAPIView, UserFullNameAPIView, UpdateInfoUserAPIView, ArtistListAPIView

urlpatterns = [
    path('get_all_users/', GetAllUsersAPIView.as_view()),
    path('profile_types/', UserProfileTypesAPIView.as_view()),
    path('user_info/<str:username>/', UserInfoAPIView.as_view()),
    path('get_full_names_of_users/', UserFullNameAPIView.as_view()),
    path('uppdate_user_profile/', UpdateInfoUserAPIView.as_view()),
    path('artists/', ArtistListAPIView.as_view()),
]
