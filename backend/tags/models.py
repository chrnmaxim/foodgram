from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True
    )
    slug = models.SlugField(
        'Слаг',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True
    )

    class Meta:
        """Внутренний класс модели тега."""

        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        """Определяет отображение наименования тега в админ-панели."""

        return f'{self.name}_{self.slug}'[:settings.ADMIN_CHARS_LIMIT]


class TagInRecipe(models.Model):
    """Модель тегов в рецептах."""

    tag = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.SET_NULL,
        related_name='tags_in_recipe',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='tags_in_recipe'
    )

    def __str__(self):
        """Определяет отображение тегов в рецептах в админ-панели."""

        return f'{self.recipe.name}_{self.recipe.name}'[:settings.ADMIN_CHARS_LIMIT]
