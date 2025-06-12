"""
Serializers for tag
"""
from rest_framework import serializers
from core.models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

    name = serializers.CharField(required=True, allow_blank=False)