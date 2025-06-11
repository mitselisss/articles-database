from rest_framework import serializers
from core.models import Article  # to be created

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for articles."""

    class Meta:
        model = Article
        fields = ['id', 'title', 'abstract', 'publication_date', 'main_text']
        read_only_fields = ['id', 'author']