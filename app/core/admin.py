"""
Django admin customization.
"""
from django.contrib import admin
from .models import Article, Tag, Comment

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Comment)
