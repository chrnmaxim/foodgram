from django.db import models
from django.conf import settings


class Unit(models.Model):
    """Модель единицы измерения."""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True
    )

    class Meta:
        """Внутренний класс модели единицы измерения."""

        verbose_name = 'единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ('name',)

    def __str__(self):
        """Определяет отображение наименования единицы измерения в админ-панели."""

        return self.name[:settings.ADMIN_CHARS_LIMIT]


class Ingredient(models.Model):
    """Модель ингридиента."""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True
    )
    measurement_unit = models.ForeignKey(
        Unit,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Единица измерения',
        related_name="ingredients_in_recipe"
    )

    class Meta:
        """Внутренний класс модели ингридиента."""
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name[:settings.ADMIN_CHARS_LIMIT]


class IngredientInRecipe(models.Model):
    """Модель ингридиентов в рецептах."""

    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ingredients_in_recipe',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='ingredients_in_recipe',
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(
        'Количество'
    )

    class Meta:
        """Внутренний класс модели ингридиентов в рецептах."""
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ['ingredient']

    def __str__(self):
        """Определяет отображение ингридиентов в рецептах в админ-панели."""

        return f'{self.recipe.name}_{self.ingredient.name}'
