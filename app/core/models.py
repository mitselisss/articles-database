"""
Database models.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    """Tag model."""
    name = models.CharField(max_length=255, unique=True, default="Tag name to be added")

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article model."""
    authors = models.ManyToManyField(User, related_name="articles")
    title = models.CharField(max_length=255, default="Title to be added")
    main_text = models.TextField(default="Full text to be added")
    abstract = models.TextField(default="Abstract to be added")
    publication_date = models.DateField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    # TODO: Add comments (related model)

    def __str__(self):
        return self.title
