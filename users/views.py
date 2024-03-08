from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .serializers import UserProfileSerializer, UserSerializer


class CreateUserAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=data.get("username"),
                password=data.get("password"),
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
            )
            profile_data = {
                "user": user.id,
                "profile_type": data.get("profile_type"),
                "phone_number": data.get("phone_number"),
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
                response_data = {
                    "user": serializer.data,
                    "profile": profile_serializer.data,
                }
                return Response(
                    {"success": True, "data": response_data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                user.delete()
                return Response(
                    profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        users = User.objects.all()
        usernames = [user["username"] for user in UserSerializer(users, many=True).data]
        return Response({"success": True, "data": usernames})


class GetTokenForUserAPIView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            return Response({"success": True, "msg": "invalid password or username"})
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        response = {"access": str(access_token), "refresh": str(refresh_token)}
        return Response({"success": True, "tokens": response})
