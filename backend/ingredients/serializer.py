from ingredients.models import Ingredient, IngredientInRecipe
from rest_framework import serializers


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
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "amount")

    def validate(self, data):
        if data['amount'] < 1:
            raise serializers.ValidationError(
                'Количество ингредиентов не может менее 1.'
            )
        return data
