from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)

from ingredients.models import IngredientInRecipe
from tags.models import Tag


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название',
        max_length=settings.MAX_FIELD_LENGTH
    )
    text = models.TextField(
        'Основной текст'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        blank=True,
        db_index=True,
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        IngredientInRecipe,
        related_name="recipes",
        blank=True,
        db_index=True,
        verbose_name='Ингредиенты'
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
        'Время приготовления',
        validators=[
            MinValueValidator(10),
            MaxValueValidator(60 * 24),
        ],
        db_index=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Внутренний класс модели рецептов для отображения в админ-панели."""

        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('id',)

    def __str__(self):
        """Определяет отображение название рецепта в админ-панели."""

        return self.name[:settings.ADMIN_CHARS_LIMIT]
