"""
Serializers for comment
"""
from rest_framework import serializers
from core.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'author']
        read_only_fields = ['id', 'author']
