"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Article, Tag
from datetime import date


class UserTests(TestCase):
    """Test for Django User model although it is not needed."""
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('testpass123'))


class ArticleTest(TestCase):
    """Test for Article model."""
    def test_create_article(self):
        """Test creating an article is successfull."""
        user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            password='password1234',
        )
        article = Article.objects.create(
            title='Sample title',
            abstract='Sample abstract',
            publication_date=date.today()
        )
        article.authors.set([user])
        self.assertEqual(str(article), article.title)
        self.assertEqual(list(article.authors.all()), [user])

    def test_update_article(self):
        """Test creating an article is successfull."""
        user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            password='password1234',
        )
        article = Article.objects.create(
            title='Original title',
            abstract='Sample abstract',
            publication_date=date.today()
        )
        article.authors.set([user])
        article.title = 'Updated title'
        article.save()
        self.assertEqual(article.title, 'Updated title')

    def test_delete_article(self):
        """Test creating an article is successfull."""
        user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            password='password1234',
        )

        article = Article.objects.create(
            title='Sample title',
            abstract='Sample abstract',
            publication_date=date.today()
        )
        article.authors.set([user])
        article_id = article.id
        article.delete()
        exist = Article.objects.filter(id=article_id).exists()
        self.assertFalse(exist)


class TagModelTest(TestCase):
    """Test for Tag model."""
    def test_create_tag(self):
        """Test creating a tag is successful."""
        tag = Tag.objects.create(name='Science')
        self.assertEqual(str(tag.name), 'Science')

    def test_update_tag(self):
        """Test updating a tag name."""
        tag = Tag.objects.create(name='OldName')
        tag.name = 'NewName'
        tag.save()
        self.assertEqual(tag.name, 'NewName')

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(name='ToDelete')
        tag_id = tag.id
        tag.delete()
        exists = Tag.objects.filter(id=tag_id).exists()
        self.assertFalse(exists)