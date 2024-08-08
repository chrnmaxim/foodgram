from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from favorite.models import Favorite
from ingredients.models import IngredientInRecipe
from ingredients.serializer import (AddIngredientSerializer,
                                    ListIngredientsSerializer)
from recipes.models import Recipe, ShoppingCartIngredients
from tags.models import Tag
from tags.serializer import TagsSerializer
from users.models import User
from users.serializers import UserCustomSerializer


class RecipesSerializerGet(serializers.ModelSerializer):
    """Сериализатор получения рецептов."""

    tags = TagsSerializer(many=True, read_only=True)
    author = UserCustomSerializer(read_only=True)
    ingredients = ListIngredientsSerializer(
        many=True, source='recipeingredient'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe_id=data.id
        ).exists()

    def get_is_in_shopping_cart(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCartIngredients.objects.filter(
            user=request.user,
            recipe_id=data.id
        ).exists()


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецептов."""

    image = Base64ImageField()
    ingredients = AddIngredientSerializer(many=True)
    tags = serializers.SlugRelatedField(
        slug_field='id', queryset=Tag.objects.all(), many=True, required=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'image', 'name', 'text', 'cooking_time',
            'ingredients', 'tags',
        )
        extra_kwargs = {'image': {'required': True}}

    def to_representation(self, instance):
        return RecipesSerializerGet(instance, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self.list_ingredients_create(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().update(instance, validated_data)
        if ingredients:
            recipe.ingredients.clear()
            self.list_ingredients_create(ingredients, recipe)
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        return recipe

    def validate(self, value):
        if not value.get('image'):
            raise serializers.ValidationError(
                'Изображение не добавлено.'
            )
        tags = value.get('tags')
        ingredients = value.get('ingredients')
        if not tags:
            raise serializers.ValidationError(
                'Теги не указаны.'
            )
        if not ingredients:
            raise serializers.ValidationError(
                'Ингредиенты не добавлены.'
            )
        if len(set(tags)) != len(tags):
            raise serializers.ValidationError(
                'Теги не должны повторяться.'
            )
        list_id_ingredients = [ingredient['id'] for ingredient in ingredients]
        if len(list_id_ingredients) != len(set(list_id_ingredients)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        return value

    def list_ingredients_create(self, ingredients, recipe):
        IngredientInRecipe.objects.bulk_create(
            [
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount'],
                )
                for ingredient in ingredients
            ]
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор получения сокращенной информации о рецептах."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор добавления рецепта в список покупок."""

    class Meta:
        fields = ('user', 'recipe')
        model = ShoppingCartIngredients
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingCartIngredients.objects.all(),
                fields=('user', 'recipe')
            ),
        )

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe, context={'request': self.context.get('request')}
        ).data


class DownloadShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    shopping_cart = serializers.FileField()

    class Meta:
        fields = ('user', 'recipe', 'shopping_cart')
        model = ShoppingCartIngredients
