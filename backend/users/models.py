from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ.'
        )],
        error_messages={
            'unique': 'Имя пользователя уже существует.'
        }
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_FIELD_LENGTH
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True
    )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
    )
    avatar = models.ImageField(
        upload_to='media/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"]),
        ],
    )

    class Meta:
        """Внутренний класс кастомной модели пользователя."""

        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        """Определяет отображение имени пользователя в админ-панели."""

        return self.username[:settings.ADMIN_CHARS_LIMIT]

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором
        или суперпользователем.
        """

        return self.role == self.ADMIN or self.is_superuser or self.is_staff
