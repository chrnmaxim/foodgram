from django.contrib import admin

from ingredients.models import Ingredient, IngredientInRecipe, Unit


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Определяет отображение ингредиентов в панели администратора."""

    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Определяет отображение единицы измерения в панели администратора."""

    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    pass
