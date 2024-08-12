from django.conf import settings
from django.db import models


class Favorite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        """Внутренний класс модели избранных рецептов."""
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('-id',)

    def __str__(self):
        """Определяет отображение рецепта в админ-панели."""
        return (
            f'{self.user.username} добавил в ' f'избранное {self.recipe.name}'
        )
