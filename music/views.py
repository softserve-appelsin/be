from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TrackSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Track
from .permissions import IsArtist
from django.http import FileResponse
from rest_framework import status


class ListTrackAPIView(APIView):
    def get(self, request):
        tracks = Track.objects.all()
        serializers_track = TrackSerializer(tracks, many=True)
        titles = [track_data['title'] for track_data in serializers_track.data]
        return Response({"success": True, "data": titles})
    

class CreateTrackAPIView(APIView):
    
    def post(self, request):
        serializer = TrackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "msg": "Track recorded"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AllTracksAPIView(APIView):

    def get(self, request):
        track = Track.objects.get(user=1)
        track_file = track.file
        response = FileResponse(open(track_file.path, 'rb'), content_type='audio/mp3')
        response['Content-Disposition'] = f'attachment; filename="{track_file.name}"'
        return response
        
        