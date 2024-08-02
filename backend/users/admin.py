from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Определяет отображение пользователей в панели администратора."""

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    list_editable = ('role',)
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
