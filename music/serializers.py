from rest_framework import serializers
from .models import Track, Album, PlayList, Comment
from django.contrib.auth.models import User

class TrackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Track
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class TrackInfoSerializer(serializers.ModelSerializer):
    artist = UserSerializer(source='user')

    class Meta:
        model = Track
        fields = ['id', 'artist', 'title', 'album', 'create_at', 'plays_count', 'likes_count', 'user_of_likes']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Album
        fields = '__all__'


class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = PlayList
        fields = '__all__'


class PlayListInfoSerializer(serializers.ModelField):
    class Meta:
        model = PlayList



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'