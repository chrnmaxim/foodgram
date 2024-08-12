# Generated by Django 5.0.7 on 2024-08-12 18:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название"),
                ),
                ("text", models.TextField(verbose_name="Основной текст")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="recipes/images/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png"]
                            )
                        ],
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "cooking_time",
                    models.PositiveSmallIntegerField(
                        db_index=True,
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                message="Время приготовления не может быть менее 1 минуты.",
                            ),
                            django.core.validators.MaxValueValidator(
                                2880,
                                message="Время приготовления не может быть более 48.0 часов.",
                            ),
                        ],
                        verbose_name="Время приготовления, мин",
                    ),
                ),
                (
                    "pub_date",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "рецепт",
                "verbose_name_plural": "Рецепты",
                "ordering": ("-pub_date",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingCartIngredients",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "рецепт в списке покупок",
                "verbose_name_plural": "Рецепты в списке покупок",
                "ordering": ("recipe",),
            },
        ),
    ]
