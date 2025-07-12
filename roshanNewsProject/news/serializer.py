from rest_framework import serializers
from .models import News, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )
    class Meta:
        model = News
        fields = ['id', 'title', 'content_news', 'tags', 'reference']
