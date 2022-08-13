from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.is_admin


class IsAdministratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, _):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, _):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, _, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)
