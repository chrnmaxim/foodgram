from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer
from ingredients.models import IngredientInRecipe
from recipes.models import Recipe
from recipes.serializers import (RecipesSerializer, RecipesSerializerGet,
                                 ShoppingCartIngredientsSerializer)
from utils.filters import RecipeFilter
from utils.pagination import PageLimitPagination
from utils.permissions import RecipePermissions

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    """ViewSet управления рецептами."""

    queryset = Recipe.objects.all()
    pagination_class = PageLimitPagination
    filterset_class = RecipeFilter
    permission_classes = [RecipePermissions]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipesSerializerGet
        return RecipesSerializer

    @action(
        detail=False,
        methods=['GET'],
        pagination_class=None,
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.user_shopping.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        list_recipes = (
            IngredientInRecipe.objects.filter(
                recipe__recipe_download__user=user
            )
            .values('ingredient__name', 'ingredient__measurement_unit__name')
            .annotate(amount=Sum('amount'))
        )
        filename = f'{user.email}ingredients.txt'
        content = '\n'.join(
            [
                f'{ingredient["ingredient__name"]} -'
                f' {ingredient["amount"]}'
                f' {ingredient["ingredient__measurement_unit__name"]}'
                for ingredient in list_recipes
            ]
        )
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = get_object_or_404(User, id=request.user.id)
        shopping_cart = ShoppingCartIngredientsSerializer.objects.filter(
            user=user.id, recipe=recipe
        )
        if request.method == 'POST':
            serializer = ShoppingCartIngredientsSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = get_object_or_404(User, id=request.user.id)
        shopping_cart = Favorite.objects.filter(user=user.id, recipe=recipe)
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['GET'],
        url_name='get_link',
        url_path='get-link',
    )
    def get_link(self, request, pk):
        get_object_or_404(Recipe, id=pk)
        link = request.build_absolute_uri(f'/recipes/{pk}/')
        return Response({'short-link': link}, status=status.HTTP_200_OK)
