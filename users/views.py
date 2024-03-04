from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User


class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile_data = {
                'user': user.id,
                'profile_type': request.data.get('profile_type')
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                response_data = {
                    'user': serializer.data,
                    'profile': profile_serializer.data
                }
                return Response({'success': True, 'data': response_data}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        usernames = [user['username'] for user in UserSerializer(users, many=True).data]
        return Response({'success': True, 'data': usernames})