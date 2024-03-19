from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import TrackSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Track
from .permissions import IsArtist

class ListTrackAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        tracks = Track.objects.all()
        serializers_track = TrackSerializer(tracks, many=True)
        print(type(serializers_track))
        return Response({"success": True, "data": serializers_track.data})
    

class CreateTrackAPIView(APIView):
    
    def post(self, request):
        permission = IsArtist.has_permission(self, request)
        if permission == False:
            return Response({"success": False, "msg": "you are not artist"})
        return Response({"success": True, "msg": "track recorded"})
        
        
        