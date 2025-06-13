"""
Test for comment api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Article, Comment
from comment.serializers import CommentSerializer
from datetime import date


COMMENT_LIST_URL = reverse('comment:comment-list')


def create_user(**params):
    return get_user_model().objects.create(**params)


def create_article(authors, **params):
    default = {
        'title': 'sample title',
        'abstract': 'sample abstract',
        'publication_date': date.today(),
        'main_text': 'sample main text'
    }
    default.update(params)
    article = Article.objects.create(**default)
    article.authors.set(authors if isinstance(authors, list) else [authors])
    return article


def create_comment(article, author, **params):
    default = {'content': 'sample content'}
    default.update(params)
    return Comment.objects.create(article=article, author=author, **default)


class PublicCommentApiTests(TestCase):
    """Test the unauthorized user tag api."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_create(self):
        """Test authorization required for tag creation."""
        article = Article.objects.create(
            title='Sample title',
            abstract='Sample abstract',
            publication_date=date.today(),
            main_text='Sample main text'
        )
        payload = {
            'content': 'sample_content',
            'article': article.id
        }
        res = self.client.post(COMMENT_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments(self):
        """Test everyone can list comments."""
        user = create_user(username='user1', email='user1@example.com', password='password1234')
        article = create_article(authors=user)
        other_user = create_user(username='user2', email='user2@example.com', password='password1234')
        create_comment(author=user, article=article, content='content1')
        create_comment(author=other_user, article=article, content='content2')
        res =  self.client.get(COMMENT_LIST_URL)
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


class PrivateTagApiTests(TestCase):
    """Test the authorized user tag api."""
    def setUp(self):
        self.user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_comment_successful(self):
        """Test creating a tag returns succesful"""
        article = create_article(authors=self.user)
        payload = {
            'content': 'sample content',
            'article': article.id
        }
        res = self.client.post(COMMENT_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(content=payload['content']).exists())

    def test_delete_own_comment(self):
        """Test that user can delete their own comment."""
        article = create_article(authors=self.user)
        comment = create_comment(article=article, author=self.user)
        url = reverse('comment:comment-detail', args=[comment.id])

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_cannot_delete_other_users_comment(self):
        """Test that users cannot delete someone else's comment."""
        article = create_article(authors=self.user)
        other_user = create_user(username='user2', email='user2@example.com', password='pass')
        comment = create_comment(article=article, author=other_user)
        url = reverse('comment:comment-detail', args=[comment.id])

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())

    def test_update_own_comment(self):
        """Test that a user can update their own comment."""
        article = create_article(authors=self.user)
        comment = create_comment(article=article, author=self.user, content='Original content')
        url = reverse('comment:comment-detail', args=[comment.id])
        payload = {'content': 'Updated content'}
        res = self.client.patch(url, payload)
        comment.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.content, payload['content'])

    def test_cannot_update_other_users_commment(self):
        """Test that a user cannot update another user's comment."""
        article = create_article(authors=self.user)
        other_user = create_user(username='user2', email='user2@example.com', password='password1234')
        comment = create_comment(author=other_user, article=article, content='original')
        url = reverse('comment:comment-detail', args=[comment.id])
        payload = {'content': 'updated'}
        res = self.client.patch(url, payload)
        comment.refresh_from_db
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(comment.content, payload['content'])

