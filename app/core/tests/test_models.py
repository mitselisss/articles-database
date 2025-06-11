"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Article
from datetime import date


class UserTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='testpass123'
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password('testpass123'))


class ArticleTest(TestCase):
    def test_create_article(self):
        """Test creating an article is successfull."""
        user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            password='password1234',
        )
        article = Article.objects.create(
            author=user,
            title='Sample title',
            abstract='Sample abstract',
            publication_date=date.today()
        )
        self.assertEqual(str(article), article.title)
        self.assertEqual(article.author, user)

    def test_update_article(self):
        """Test creating an article is successfull."""
        user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            password='password1234',
        )
        article = Article.objects.create(
            author=user,
            title='Original title',
            abstract='Sample abstract',
            publication_date=date.today()
        )
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
            author=user,
            title='Sample title',
            abstract='Sample abstract',
            publication_date=date.today()
        )

        article_id = article.id
        article.delete()
        exist = Article.objects.filter(id=article_id).exists()
        self.assertFalse(exist)