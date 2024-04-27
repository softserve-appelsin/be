from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class CreateUserAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=data.get('username'), 
                password=data.get('password'), 
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
                )
            profile_data = {
                'user': user.id,
                'profile_type': data.get('profile_type'),
                'phone_number': data.get('phone_number')
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                response_data = {
                    'user': serializer.data,
                    'profile': profile_serializer.data
                }
                return Response({"success": True, 'data': response_data}, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
     
class RefreshTokenAPIView(APIView):
    
    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh_token'])
            access_token = token.access_token
            new_refresh_token = token
            return Response({
                "success": True,
                'access_token': str(access_token),
                'refresh_token': str(new_refresh_token),
            })
        except Exception as e:
            return Response({"error": str(e)})


class GetTokenForUserAPIView(APIView):
    
    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            return Response({"success": False, 'msg': 'Invalid password or username'})
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        access_token.payload['user_id'] = user.id
        access_token.payload['username'] = user.get_username()
        access_token.payload['profile_type'] = user.profile.profile_type
        
        refresh_token.payload['user_id'] = user.id
        refresh_token.payload['username'] = user.get_username()
        refresh_token.payload['profile_type'] = user.profile.profile_type
        
        response = {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }
        return Response({"success": True, 'tokens': response})


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
