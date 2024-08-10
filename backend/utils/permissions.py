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

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )



# class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Разрешены только безопасные методы,
#     а также доступ суперпользователю или автору объекта.
#     """

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_admin
#             or request.user.is_moderator
#             or obj.author == request.user
#         )
