from django_filters.rest_framework import FilterSet, filters

from ingredients.models import Ingredient
from recipes.models import Recipe
from tags.models import Tag


class NameFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug', to_field_name='slug',
        lookup_expr='istartswith',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, values):
        user = self.request.user
        if values and not user.is_anonymous:
            return queryset.filter(recipe_favorite__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, values):
        user = self.request.user
        if values and not user.is_anonymous:
            return queryset.filter(recipe_download__user_id=user.id)
        return queryset
