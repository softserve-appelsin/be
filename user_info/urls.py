from django.urls import path
from .views import GetAllUsersAPIView, UserProfileTypesAPIView, \
    UserInfoAPIView, UserFullNameAPIView, UpdateInfoUserAPIView, ArtistListAPIView

urlpatterns = [
    path('get_all_users/', GetAllUsersAPIView.as_view(), name='all-users-on-web-app'),
    path('profile_types/', UserProfileTypesAPIView.as_view(), name='all-users-type-of-account'),
    path('user_info/<str:username>/', UserInfoAPIView.as_view(), name='whole-info-about-user'),
    path('get_full_names_of_users/', UserFullNameAPIView.as_view(), name='useless'),
    path('uppdate_user_profile/', UpdateInfoUserAPIView.as_view(), name='update-profile-info'),
    path('artists/', ArtistListAPIView.as_view(), name='list-all-artist'),
    path('artists/<int:pk>/', ArtistListAPIView.as_view(), name='certain-artist-info'),
]
