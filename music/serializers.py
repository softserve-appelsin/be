from rest_framework import serializers
from .models import Track, Album, PlayList, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TrackSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Track
        fields = '__all__'

class TrackInfoSerializer(serializers.ModelSerializer):
    artist = UserSerializer(source='user')

    class Meta:
        model = Track
        fields = ['artist', 'title', 'album', 'create_at', 'plays_count', 'likes_count', 'user_of_likes']

class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Album
        fields = '__all__'


class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PlayList
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'