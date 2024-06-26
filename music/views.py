from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrackSerializer, PlayListSerializer, TrackInfoSerializer, AlbumSerializer, PlayListInfoSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Track, PlayList, Album
from .permissions import IsArtist
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from .utils import get_track_file_from_aws
from django.contrib.auth.models import User
from django.http import Http404

class TrackAPIView(APIView):
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, IsArtist, ]
        return [permission() for permission in permission_classes]

    
    
    def get(self, request):
        track_id = request.query_params.get('track_id_file')
        track_id_info = request.query_params.get('track_id')
        track_name = request.query_params.get('track_name')
        
        if track_name:
            track = Track.objects.filter(title__icontains=track_name)
            serializer = TrackSerializer(track, many=True)
            return Response({"success": True, "data": serializer.data})
        
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
        title = request.data.get('title')
        user = request.user
        existing_track = Track.objects.filter(user=user, title=title).exists()
        if existing_track:
            return Response({"success": False, "msg": "This track already exists for the user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TrackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "Track recorded"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request):
        try:
            track_id = request.data.get('track_id')
            if track_id:
                title = request.data['title']
                track = Track.objects.get(id=track_id)
                serializer = TrackSerializer(track)
                serializer.update()

                return Response({"success": True, "message": f"updated title: {title}"})
        except Track.DoesNotExist as e:
            return Response({'status_code': 404, "message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status_code': 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
            
    def delete(self, request, pk=None):
        if pk:
            try:
                track = get_object_or_404(Track, id=pk, user=request.user)
                track.delete()
                return Response({"success": True, "msg": "Track deleted"}, status=status.HTTP_204_NO_CONTENT)
            except Track.DoesNotExist:
                return Response({"success": False, "msg": "Track does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"success": False, "msg": "Track id is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)
    
class TrackByArtistAPIView(APIView):
    
    permission_classes = [IsArtist, ]
    
    def get(self, request):
        try:
            user = request.user
            tracks = Track.objects.filter(user=user)
            serializer = TrackSerializer(tracks, many=True, context={'request': request})
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        

class AlbumByArtistAPIView(APIView):
    
    permission_classes = [IsArtist, ]
    
    def get(self, request):
        try:
            user = request.user
            tracks = Album.objects.filter(user=user)
            serializer = AlbumSerializer(tracks, many=True, context={'request': request})
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        

class PlayListAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request, pk=None):
        playlist_name = request.query_params.get('playlist_name')
        playlist = request.query_params.get('playlsit')
        
        if playlist_name:
            try:
                playlist = PlayList.objects.filter(title__icontains=playlist_name, user=request.user)
                serializer = PlayListSerializer(playlist, many=True)
                return Response({'success': True, 'data': serializer.data})
            except Exception as e:
                return Response({"success": False, "message": str(e)})
        
        if pk:
            try:
                playlist = PlayList.objects.get(id=pk, user=request.user)
                serializer = PlayListInfoSerializer(playlist)
                return Response({'success': True, 'data': serializer.data})
            except Exception as e:
                return Response({"success": False, "message": str(e)})
            
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
    
    def delete(self, request, pk=None):
        if pk:
            try:
                playlist = get_object_or_404(PlayList, id=pk, user=request.user)
                playlist.delete()
                return Response({"success": True, "msg": "Playlist deleted"}, status=status.HTTP_204_NO_CONTENT)
            except PlayList.DoesNotExist:
                return Response({"success": False, "msg": "Playlist does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"success": False, "msg": "Playlist ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)


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
    
    def get(self, request, pk=None):
        
        album_name = request.query_params.get('album_name')
        
        if album_name:
            playlist = Album.objects.filter(name__icontains=album_name)
            serializer = AlbumSerializer(playlist, many=True)
            return Response({'success': True, 'data': serializer.data})
        
        if pk:
            try:
                current_album = Album.objects.get(id=pk)
                tracks_in_album = Track.objects.filter(album=current_album)
                serializer = AlbumSerializer(current_album)
                tracks = TrackInfoSerializer(tracks_in_album, many=True)
                return Response({"success": True, "data": {
                    'album': serializer.data,
                    'tracks': tracks.data
                }})
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
        
        
    def put(self, request, pk=None):
        if not pk:
            return Response({"success": False, "msg": "Album id is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            album = Album.objects.get(id=pk, user=request.user)
        except Album.DoesNotExist:
            return Response({"success": False, "msg": 'Album does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        track_id = request.data.get('track_id')
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            return Response({"success": False, "msg": 'Track does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TrackSerializer(track, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(album=album)  # Associate track with the album
            return Response({"success": True, "msg": "Track added to album"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk=None):
        if pk:
            try:
                album = get_object_or_404(Album, id=pk, user=request.user)
                album.delete()
                return Response({"success": True, "msg": "Album deleted"}, status=status.HTTP_204_NO_CONTENT)
            except Album.DoesNotExist:
                return Response({"success": False, "msg": "Album does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"success": False, "msg": "Album id is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)


class TrackAlbumPageArtistAPIView(APIView):
    
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, id):
        try: 
            user = get_object_or_404(User, id=id)
            tracks = Track.objects.filter(user=user)
            albums = Album.objects.filter(user=user)
            
            tracks_serializer = TrackSerializer(tracks, many=True)
            albums_serializer = AlbumSerializer(albums, many=True)
            
            return Response({"success": True,
                             "data": {
                                "tracks": tracks_serializer.data,
                                "albums": albums_serializer.data
                             }
                           })

        except Http404:
            return Response({"success": False, "message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        