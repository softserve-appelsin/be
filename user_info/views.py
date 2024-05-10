from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserProfileSerializer
from users.models import Profile
from rest_framework.permissions import IsAuthenticated
from music.models import PlayList, Track
from music.serializers import PlayListSerializer, TrackSerializer
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404


class UserInfoAPIView(APIView):
    def get(self, request, username):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({"success": False, "message": f"User with username '{username}' not found"},
                            status=status.HTTP_404_NOT_FOUND)

        playlists = PlayList.objects.filter(user=profile.user)
        playlist_serializer = PlayListSerializer(playlists, many=True)

        favorite_tracks = Track.objects.filter(user=profile.user, likes_count__gt=0)
        favorite_tracks_serializer = TrackSerializer(favorite_tracks, many=True)

        user_info = {
            "username": profile.user.username,
            "profile_type": profile.profile_type,
            "phone_number": profile.phone_number,
            "bio": profile.bio,
            "playlists": playlist_serializer.data,
            "favorite_tracks": favorite_tracks_serializer.data
        }

        return Response({"success": True, "user_info": user_info})
    
    
class GetAllUsersAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        users = User.objects.all()
        usernames = [user['username'] for user in UserSerializer(users, many=True).data]
        return Response({"success": True, "data": usernames})


class UserProfileTypesAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        profile_types = [profile_data['profile_type'] for profile_data in serializer.data]
        return Response({"success": True, "profile_types": profile_types})
    

class UserFullNameAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        users = User.objects.all()
        full_name = []
        for user in users:
            full_name.append({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            })
        if full_name == None:
            return Response({"success": True, "detail": "User Full Name doesn’t exist"})
        return Response({"success": True, "full_name": full_name})


class UpdateInfoUserAPIView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_profile = self.request.user.profile
        return user_profile

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)


class ArtistListAPIView(APIView):
    
    def get(self, request, pk=None):
            
        if pk:
            user = get_object_or_404(User, id=pk)
            profile = get_object_or_404(Profile, user=user)
            
            if profile.profile_type != "Artist":
                return Response({"success": True, "msg": "current user is not artist"}, status=status.HTTP_400_BAD_REQUEST)
            
            user_serializer = UserSerializer(user)
            profile_serializer = UserProfileSerializer(profile)
            
            return Response({"success": True, "data": {
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }}, status=status.HTTP_200_OK)
         
        artists_profiles = Profile.objects.filter(profile_type="Artist")
        
        if not artists_profiles.exists():
            return Response({"message": "No artists available"}, status=status.HTTP_404_NOT_FOUND)

        users = [profile.user for profile in artists_profiles]
        user_serializer = UserSerializer(users, many=True)
        profile_serializer = UserProfileSerializer(artists_profiles, many=True)
        return Response({"success": True, "data": {
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }}, status=status.HTTP_200_OK)
