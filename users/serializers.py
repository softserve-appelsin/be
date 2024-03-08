from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
