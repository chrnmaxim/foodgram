from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientsViewSet
from recipes.views import RecipesViewSet
from tags.views import TagsViewSet
from users.views import CustomUsersViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', CustomUsersViewSet, basename='users')
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('swagger.routes')),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
