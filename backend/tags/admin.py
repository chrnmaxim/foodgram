from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Определяет отображение тегов в панели администратора."""

    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
