from django.contrib import admin
from django.urls import path, include
from .views import CreateUserAPIView

urlpatterns = [
    path('', CreateUserAPIView.as_view())
]
