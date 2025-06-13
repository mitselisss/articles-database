"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Article, Tag, Comment
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
        tag = Tag.objects.create(name='Sample_tag')
        self.assertEqual(str(tag.name), 'Sample_tag')

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


class CommentModelTest(TestCase):
    """Test for Comment model."""
    def test_create_comment(self):
        """Test creating a comment."""
        user = get_user_model().objects.create_user(
            'tester', 'tester@test.com', 'pass')
        article = Article.objects.create(
            title='Test Article',
            abstract='Test abstract',
            publication_date=date.today()
        )
        article.authors.set([user])
        comment = Comment.objects.create(
            author=user,
            article=article,
            content='Nice one!'
        )
        self.assertEqual(str(comment), 'Nice one!')
        self.assertEqual(comment.author, user)
        self.assertEqual(comment.article, article)

    def test_update_comment(self):
        """Test updating a comment."""
        user = get_user_model().objects.create_user(
            'tester', 'tester@test.com', 'pass')
        comment = Comment.objects.create(author=user, content='original')
        comment.content = 'updated'
        comment.save()
        self.assertEqual(comment.content, 'updated')

    def test_delete_comment(self):
        """Test deleting a comment."""
        user = get_user_model().objects.create_user(
            'tester', 'tester@test.com', 'pass')
        comment = Comment.objects.create(author=user, content='ToDelete')
        comment_id = comment.id
        comment.delete()
        exists = Comment.objects.filter(id=comment_id).exists()
        self.assertFalse(exists)

    def test_comment_string_representation(self):
        user = get_user_model().objects.create_user(
            username='john',
            email='john@example.com',
            password='pass1234'
        )
        comment = Comment.objects.create(
            content='this is a string!',
            author=user
        )
        self.assertEqual(str(comment), 'this is a string!')
