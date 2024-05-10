from rest_framework import serializers
from users.models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['bio', 'username', 'first_name', 'last_name']