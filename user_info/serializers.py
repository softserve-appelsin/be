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
        fields = '__all__'  


class UserAndProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'date_joined'] 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile = Profile.objects.get(user=instance)  
        profile_data = UserProfileSerializer(profile).data  
        representation['profile'] = profile_data 
        return representation
    
