from django.urls import path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title='Foodgram',
        default_version='v1',
        description='Документация проекта `Foodgram`',
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
    authentication_classes=[JWTAuthentication],
)

urlpatterns = [
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('', RedirectView.as_view(url='swagger/', permanent=False), name='index'),
]
