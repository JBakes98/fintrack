from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    message = 'Account must be verified'

    def has_permission(self, request, view):
        return request.user.is_verified
