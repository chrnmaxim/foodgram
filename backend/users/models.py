from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator, RegexValidator, validate_email
from django.db import models


class UserManager(BaseUserManager):
    """Кастомный менеджер создания пользователя."""

    use_in_migrations = True

    def _create_user(
            self, email, username,
            first_name, last_name,
            password, **extra_fields
    ):
        """Переопределение создания пользователя."""
        if not email:
            raise ValueError('Введите `email`.')
        if not username:
            raise ValueError('Введите имя пользователя.')
        if not first_name:
            raise ValueError('Введите имя.')
        if not last_name:
            raise ValueError('Введите фамилию.')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            email=email, username=username, first_name=first_name,
            last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, username,
            first_name, last_name,
            password=None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )

    def create_superuser(
            self, email, username,
            first_name, last_name,
            password, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields.get('is_superuser'):
            raise ValueError('Для суперпользователя должен быть установлен '
                             'флаг `is_superuser=True`.')
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields
        )


class User(AbstractUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = ((USER, 'Пользователь'), (ADMIN, 'Администратор'))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True,
        error_messages={'unique': 'Имя пользователя уже существует.'},
    )
    last_name = models.CharField(
        'Фамилия', max_length=settings.MAX_FIELD_LENGTH
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ.',
            )
        ],
    )
    email = models.EmailField(
        'Адрес электронной почты',
        validators=[validate_email],
        unique=True)
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
    )
    avatar = models.ImageField(
        upload_to='users/images/',
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

        return self.username[: settings.ADMIN_CHARS_LIMIT]

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором
        или суперпользователем.
        """

        return self.role == self.ADMIN or self.is_superuser or self.is_staff
