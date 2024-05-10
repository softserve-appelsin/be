from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrackSerializer, PlayListSerializer, TrackInfoSerializer, AlbumSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Track, PlayList, Album
from .permissions import IsArtist
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from .utils import get_track_file_from_aws

class TrackAPIView(APIView):
    
    def get(self, request):
        track_id = request.query_params.get('track_id_file')
        track_id_info = request.query_params.get('track_id')
        
        if track_id:
            try:
                track = get_object_or_404(Track, id=track_id)
                obj = get_track_file_from_aws(track)
                
                track.plays_count += 1
                track.save()
                
                return FileResponse(obj, filename=track.file.name)

            except Track.DoesNotExist:
                return Response("Track does not exist", status=404)
            except Exception as e:
                return Response(str(e), status=500)
            
        if track_id_info:
            try:
                track = get_object_or_404(Track, id=track_id_info)
                
                liked_song = track.user_of_likes.filter(id=request.user.id).exists() 
                serializers = TrackInfoSerializer(track)

                return Response({"success": True,  "data": serializers.data, "liked": liked_song})
            
            except Track.DoesNotExist:
                return Response({"success": False, "msg": "Track does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            except Exception as e:
                return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        tracks = Track.objects.all()
        serializers_track = TrackInfoSerializer(tracks, many=True)
        return Response({"success": True, "data": serializers_track.data})
    
    
    def post(self, request):
        serializer = TrackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "Track recorded"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackByArtistAPIView(APIView):
    
    permission_classes = [IsArtist, ]
    
    def get(self, request):
        try:
            user = request.user
            tracks = Track.objects.filter(user=user)
            serializer = TrackSerializer(tracks)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        

class AlbumByArtistAPIView(APIView):
    
    permission_classes = [IsArtist, ]
    
    def get(self, request):
        try:
            user = request.user
            tracks = Album.objects.filter(user=user)
            serializer = AlbumSerializer(tracks)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        

class PlayListAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        try:
            playlist = PlayList.objects.filter(user=request.user)
            
        except ObjectDoesNotExist as e:
            return Response({"success": True, "msg": "no playlists for current user"})
        
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        
        serializer = PlayListSerializer(playlist, many=True)
        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        data = request.data
        serializer = PlayListSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "playlist created"})
        return Response({"success": False})


    def put(self, request):
        playlist_id = request.data.get('playlist_id')
        track_ids = request.data.get('track_ids')
        if not playlist_id or not track_ids:
            return Response({"success": False, "msg": "Missing playlist ID or track IDs."}, status=status.HTTP_400_BAD_REQUEST)

        playlist = get_object_or_404(PlayList, pk=playlist_id)
        tracks = Track.objects.filter(pk__in=track_ids)
        playlist.tracks.add(*tracks) 
        return Response({"success": True, "msg": "Tracks added to playlist."})


class PlayListInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = PlayList.objects.filter(user=request.user)
        serializer = PlayListSerializer(playlists, many=True)

        playlist_data = []
        for playlist in playlists:
            tracks_count = playlist.tracks.count()
            playlist_data.append({
                "id": playlist.id,
                "title": playlist.title,
                "tracks_count": tracks_count,
            })

        return Response({
            "success": True,
            "data": {
                "playlists": serializer.data,
                "count_playlists": playlists.count(),
                "playlist_info": playlist_data
            }
        })
        
        
class TrackLikeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        user = request.user
        liked_tracks = Track.objects.filter(user_of_likes=user)
        serialized_tracks = TrackSerializer(liked_tracks, many=True)  
        return Response({"success": True, "data": serialized_tracks.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        track_id = request.data.get('track_id')

        try:
            track = Track.objects.get(pk=track_id)
        except Track.DoesNotExist:
            return Response({"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND)

        if user in track.user_of_likes.all():
            return Response({"error": "You have already liked this track."}, status=status.HTTP_400_BAD_REQUEST)

        track.likes_count += 1
        track.user_of_likes.add(user)
        track.save()

        return Response({"message": "Track liked successfully"}, status=status.HTTP_200_OK)
    
    
    def put(self, request):
        user = request.user
        track_id = request.data.get('track_id')

        try:
            track = Track.objects.get(pk=track_id)
        except Track.DoesNotExist:
            return Response({"error": "Track not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in track.user_of_likes.all():
            return Response({"error": "You have not liked this track."}, status=status.HTTP_400_BAD_REQUEST)

        track.likes_count -= 1
        track.user_of_likes.remove(user)
        track.save()

        return Response({"message": "Like removed successfully"}, status=status.HTTP_200_OK)
    

class AlbumAPIView(APIView):
    
    def get(self, request, album=None):
        
        if album:
            try:
                current_album = Album.objects.get(name=album)
                serializer = AlbumSerializer(current_album)
                return Response({"success": True, "data": serializer.data})
            except Album.DoesNotExist:
                return Response({"success": False, "msg": 'album does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        tracks = Album.objects.all()
        serializers_track = AlbumSerializer(tracks, many=True)
        return Response({"success": True, "data": serializers_track.data})
    
    
    def post(self, request):
        data = request.data
        serializer = AlbumSerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "album created"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request):
        return Response({"success": True, "request": request})


class TrackAlbumPageArtistAPIView(APIView):
    
    def get(request, self, id):
        try: 
            tracks = Track.objects.filter(user=id)
            album = Album.objects.filter(user=id)
            
            tracks_serializer = TrackSerializer(tracks, many=True)
            albums_serializer = AlbumSerializer(album, many=True)
            
            return Response({"success": True,
                             "data": {
                                "tracks": tracks_serializer.data,
                                "albums": albums_serializer.data
                    }
                }
            )

        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        