from rest_framework import viewsets

from tags.models import Tag
from tags.serializer import TagsSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для получения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
