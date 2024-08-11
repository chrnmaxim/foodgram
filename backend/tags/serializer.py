from rest_framework import serializers
from tags.models import Tag


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        fields = ('id', 'name', 'slug')
        model = Tag
        lookup_field = 'id'
