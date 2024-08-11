from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CustomPermissions(BasePermission):
    """
    Ограничение прав конфигурации `Djoser`.

    Устанавливается на уровне проекта.
    """

    def has_permission(self, request, view):
        if request.method in ['list', 'retrieve', 'GET']:
            return 'rest_framework.permissions.AllowAny'


class RecipePermissions(BasePermission):
    """Ограничение для эндпоинтов `recipes`."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or obj.author == request.user
            or request.user.is_authenticated
        )
