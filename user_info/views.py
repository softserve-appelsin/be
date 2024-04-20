from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from users.serializers import UserSerializer, UserProfileSerializer
from users.models import Profile
from users.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from music.models import PlayList, Track
from music.serializers import PlayListSerializer, TrackSerializer
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView


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
            "avatar": str(profile.avatar),
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
        return Response({"success": True, 'data': usernames})


class UserProfileTypesAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        profile_types = [profile_data['profile_type'] for profile_data in serializer.data]
        return Response({'success': True, 'profile_types': profile_types})
    

class UserFullNameAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        users = User.objects.all()
        full_name = []
        for user in users:
            full_name.append({
                'first_name': user.first_name,
                'last_name': user.last_name,
            })
        if full_name == None:
            return Response({'success': True, 'detail': 'User Full Name doesn’t exist'})
        return Response({'success': True, 'full_name': full_name})


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