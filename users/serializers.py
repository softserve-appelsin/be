from rest_framework.serializers import ModelSerializer
from .models import Profile
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'