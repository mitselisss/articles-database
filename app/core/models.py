"""
Database models.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Article(models.Model):
    """Article model."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Title to be added")
    main_text = models.TextField(default="Full text to be added")
    abstract = models.TextField(default="Abstract to be added")
    publication_date = models.DateField()
    # TODO: Add tags (ManyToManyField)
    # TODO: Add comments (related model)

    def __str__(self):
        return self.title