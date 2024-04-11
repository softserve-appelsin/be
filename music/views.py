from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrackSerializer, PlayListSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Track, PlayList
from .permissions import IsArtist
from django.http import FileResponse
from rest_framework import status
from django.shortcuts import get_object_or_404


class TrackAPIView(APIView):
    
    def get(self, request):
        track_id = request.query_params.get('track_id')
        if track_id:
            try:
                track = get_object_or_404(Track, id=track_id)
                response = FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
                track.plays_count += 1
                track.save()
                return response
            except Track.DoesNotExist:
                return Response({"success": False, "msg": "Track does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        tracks = Track.objects.all()
        serializers_track = TrackSerializer(tracks, many=True)
        return Response({"success": True, "data": serializers_track.data})
    
    
    def post(self, request):
        serializer = TrackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "Track recorded"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PlayListAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        try:
            playlist = PlayList.objects.get(user=request.user)
        except Exception as e:
            return Response({"success": False, "msg": str(e)})
        serializer = PlayListSerializer(playlist)
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
                'id': playlist.id,
                'title': playlist.title,
                'tracks_count': tracks_count,
            })

        return Response({
            "success": True,
            "data": {
                "playlists": serializer.data,
                "count_playlists": playlists.count(),
                "playlist_info": playlist_data
            }
        })