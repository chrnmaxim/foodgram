from django.contrib import admin
from recipes.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Определяет отображение рецептов в панели администратора."""

    list_display = (
        'name',
        'text',
        'cooking_time',
    )
    search_fields = ('name', 'text')
    empty_value_display = '-пусто-'
