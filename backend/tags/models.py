from django.conf import settings
from django.db import models


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        'Название', max_length=settings.MAX_FIELD_LENGTH, unique=True
    )
    slug = models.SlugField(
        'Слаг', max_length=settings.MAX_FIELD_LENGTH, unique=True
    )

    class Meta:
        """Внутренний класс модели тега."""

        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        """Определяет отображение наименования тега в админ-панели."""

        return f'{self.name}_{self.slug}'[: settings.ADMIN_CHARS_LIMIT]
