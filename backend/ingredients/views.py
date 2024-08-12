from rest_framework import viewsets

from ingredients.models import Ingredient
from ingredients.serializer import IngredientsSerializer
from utils.filters import NameFilter


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения списка ингредиентов и отдельного ингредиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    filterset_class = NameFilter
    pagination_class = None
