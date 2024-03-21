from django.contrib import admin
from django.urls import path, include
from .views import ListTrackAPIView, CreateTrackAPIView, AllTracksAPIView

urlpatterns = [
    path('all_tracks/', ListTrackAPIView.as_view()),
    path('create_track/', CreateTrackAPIView.as_view()),
    path('track/<int:pk>', AllTracksAPIView.as_view())
]
