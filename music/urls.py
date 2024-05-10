from django.urls import path
from .views import TrackAPIView, PlayListAPIView, \
    PlayListInfoAPIView, TrackLikeAPIView, AlbumAPIView, AlbumByArtistAPIView, \
        TrackByArtistAPIView, TrackAlbumPageArtistAPIView

urlpatterns = [
    path('tracks/', TrackAPIView.as_view()),
    path('playlists/', PlayListAPIView.as_view()),
    path('playlists_info/', PlayListInfoAPIView.as_view()),
    path('like_tracks/', TrackLikeAPIView.as_view()),
    path('album/', AlbumAPIView.as_view()),
    path('album/<int:pk>', AlbumAPIView.as_view()),
    path('track_by_artist/', TrackByArtistAPIView.as_view()),
    path('album_by_artis/', AlbumByArtistAPIView.as_view()),
    path('page_artist/', TrackAlbumPageArtistAPIView.as_view()),
]

