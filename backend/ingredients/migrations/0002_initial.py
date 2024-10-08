# Generated by Django 5.0.7 on 2024-08-12 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingredients", "0001_initial"),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ingredientinrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredients_in_recipe",
                to="recipes.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ingredients_in_recipe",
                to="ingredients.unit",
                verbose_name="Единица измерения",
            ),
        ),
    ]
