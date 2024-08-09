from django.contrib.auth import get_user_model
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.serializers import ShortRecipeSerializer
from subscriptions.models import Subscription
from users.serializers import UserCustomSerializer

User = get_user_model()


class SubscriptionsGetSerializer(UserCustomSerializer):
    """Сериализатор получения подписок."""

    recipes = serializers.SerializerMethodField(
        'get_recipes',
        read_only=True
    )
    recipes_count = serializers.SerializerMethodField(
        'get_recipes_count',
        read_only=True
    )

    class Meta:
        model = User
        fields = UserCustomSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar',
        )

    def get_recipes_count(self, data):
        return data.user.count()

    def get_recipes(self, data):
        request = self.context.get('request')
        recipes = data.user.all()
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = ShortRecipeSerializer(recipes, many=True)
        return serializer.data


class ListSubscriptionsSerialaizer(serializers.ModelSerializer):
    """Сериализатор создания подписок."""

    class Meta:
        fields = ('user', 'author')
        model = Subscription
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author')
            ),
        )

    def validate(self, validated_data):
        if validated_data['user'] == validated_data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return validated_data

    def to_representation(self, instance):
        return SubscriptionsGetSerializer(
            instance.author,
            context={'request': self.context.get('request')},
        ).data
