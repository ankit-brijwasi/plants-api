from rest_framework import permissions

class IsNursury(permissions.BasePermission):
    message = "Only nursuries have the permission to view this portion"

    def has_object_permission(self, request):
        return request.user.type == "nursury"