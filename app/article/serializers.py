"""
Serializers for articles
"""
from rest_framework import serializers
from core.models import Article, Tag
from django.contrib.auth import get_user_model
from tag.serializers import TagSerializer

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""
    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all()
    )
    tags = TagSerializer(many=True, required=False)


    class Meta:
        model = Article
        fields = ['id', 'title', 'abstract', 'publication_date', 'main_text', 'authors', 'tags']
        read_only_fields = ['id']


    def create(self, validated_data):
        print(f"[Serializer] In create() - Request user: {self.context['request'].user}")
        authors = validated_data.pop('authors', [])
        tags = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        article.authors.set(authors)
        for tag_dict in tags:
            tag_obj, _ = Tag.objects.get_or_create(**tag_dict)
            article.tags.add(tag_obj)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        authors = validated_data.pop('authors', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)
        if authors is not None:
            instance.authors.set(authors)

        return instance
