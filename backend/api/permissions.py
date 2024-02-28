from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        return False


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user == obj.author:
            return True

        return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user == obj.author:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
