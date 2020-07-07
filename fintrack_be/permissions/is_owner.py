from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'Not authorised to view'

    def has_object_permission(self, request, view, obj):
        # Allow logged in User to view own details, staff can view all records
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.user == request.user
        else:
            return False
