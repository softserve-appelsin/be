from rest_framework import permissions

class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.profile.profile_type == 'Artist'