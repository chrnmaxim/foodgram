from rest_framework.permissions import BasePermission


class CustomPermissions(BasePermission):
    """Ограничение прав в settings djoser.

    Передаём строкой, т.к. в настройках ожидаем тип переменной строка.
    Устанавливается на уровне проекта.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous and (
            request.method in ['list', 'retrieve', 'GET']
        ):
            return 'rest_framework.permissions.AllowAny'
