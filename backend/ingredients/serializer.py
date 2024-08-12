from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from ingredients.models import Ingredient, IngredientInRecipe


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        lookup_field = 'id'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['measurement_unit'] = f'{instance.measurement_unit.name}'
        return data


class ListIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецептах."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'measurement_unit', 'amount', 'name')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиентов в рецептах."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_AMOUNT_VALUE,
                message=('Количество игредиентов не может быть '
                         f'меньше{settings.MIN_AMOUNT_VALUE}.')
            ),
            MaxValueValidator(
                settings.MAX_AMOUNT_VALUE,
                message=('Количество игредиентов не может быть '
                         f'больше {settings.MAX_AMOUNT_VALUE}.')
            ),
        ],
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')
