from django.contrib import admin
from django.urls import path, include
from .views import TrackAPIView, PlayListAPIView

urlpatterns = [
    path('tracks/', TrackAPIView.as_view()),
    path('playlists/', PlayListAPIView.as_view())
]
