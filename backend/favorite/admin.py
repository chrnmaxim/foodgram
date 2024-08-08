from django.contrib import admin

from favorite.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Определяет отображение избранных рецептов в панели администратора."""

    list_display = ['recipe', 'author', 'pub_date']
    list_filter = ['pub_date', 'author']
    search_fields = ['recipe']
    list_display_links = ['recipe']
    readonly_fields = ['pub_date']
