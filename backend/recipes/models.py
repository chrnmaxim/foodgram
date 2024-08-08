from django.conf import settings
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models

from ingredients.models import IngredientInRecipe
from tags.models import Tag


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=settings.MAX_FIELD_LENGTH)
    text = models.TextField('Основной текст')
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        blank=True,
        db_index=True,
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        related_name="recipes",
        blank=True,
        db_index=True,
        verbose_name='Ингредиенты',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='media/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )

    cooking_time = models.PositiveIntegerField(
        'Время приготовления, мин',
        validators=[
            MinValueValidator(
                1, message='Время приготовления не может быть менее 1 минуты.'
            ),
            MaxValueValidator(
                60 * 48,
                message='Время приготовления не может быть более 2-х суток.',
            ),
        ],
        db_index=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Внутренний класс модели рецептов для отображения в админ-панели."""

        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        """Определяет отображение название рецепта в админ-панели."""

        return self.name[: settings.ADMIN_CHARS_LIMIT]


class ShoppingCartIngredients(models.Model):
    """Модель рецептов в списке покупок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_shopping',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_download',
    )

    class Meta:
        verbose_name = 'рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
