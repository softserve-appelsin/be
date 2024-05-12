from django.urls import path
from .views import TrackAPIView, PlayListAPIView, \
    PlayListInfoAPIView, TrackLikeAPIView, AlbumAPIView, AlbumByArtistAPIView, \
        TrackByArtistAPIView, TrackAlbumPageArtistAPIView

urlpatterns = [
    path('tracks/', TrackAPIView.as_view(), name='track-list-create'),
    path('tracks/<int:pk>/', TrackAPIView.as_view(), name='track-destroy'),
    path('playlists/', PlayListAPIView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>', PlayListAPIView.as_view(), name='playlist-destroy'),
    path('playlists_info/', PlayListInfoAPIView.as_view(), name='info-about-whole-playlist'),
    path('like_tracks/', TrackLikeAPIView.as_view(), name='like-and-remove-like-track'),
    path('album/', AlbumAPIView.as_view(), name='album-list-create-update'),
    path('album/<int:pk>', AlbumAPIView.as_view(), name='album-delete'),
    path('track_by_artist/', TrackByArtistAPIView.as_view(), name='tracks-by-current-request-user'),
    path('album_by_artist/', AlbumByArtistAPIView.as_view(), name='album-by-current-request-user'),
    path('page_artist/<int:id>/', TrackAlbumPageArtistAPIView.as_view(), name='list-track-and-album-by-artist-id'),
]

