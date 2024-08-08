from django.contrib import admin

from follow.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Определяет отображение подписок в панели администратора."""

    list_display = ["author", "user"]
