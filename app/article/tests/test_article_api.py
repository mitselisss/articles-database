"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Article
from article.serializers import ArticleSerializer
from datetime import date


ARTICLES_LIST_URL = reverse('article:article-list')


def create_user(**params):
    return get_user_model().objects.create(**params)

def create_article(author, **params):
    default = {
        'title': 'Sample Title',
        'abstract': 'Sample Abstract',
        'publication_date': date.today()
    }
    default.update(params)
    return Article.objects.create(author=author, **default)


class PublicArticleApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_create(self):
        payload = {
            'title': 'Unauthorized',
            'abstract': 'Should not work',
            'publication_date': '2025-01-01'
        }
        res = self.client.post(ARTICLES_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_articles(self):
        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(user, title='Article 1')
        create_article(user, title='Article 2')

        res =  self.client.get(ARTICLES_LIST_URL)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_articles_by_author(self):
        user1 = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(user1, title='Article 1')
        create_article(user1, title='Article 2')

        user2 = create_user(
            username='user2',
            email='u2@example.com',
            password='pass1234'
        )
        create_article(user2, title='Article 3')
        create_article(user2, title='Article 4')

        res =  self.client.get(ARTICLES_LIST_URL, {'author': user1.id})
        articles = Article.objects.filter(author=user1)
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_filter_articles_by_tag(self):
    #     user = create_user(
    #         username='user1',
    #         email='u1@example.com',
    #         password='pass1234'
    #     )
    #     create_article(user, title='Article 1', tag="food")
    #     create_article(user, title='Article 2', tag="food")
    #     create_article(user, title='Article 3', tag="games")
    #     create_article(user, title='Article 4', tag="sports")

    #     res =  self.client.get(ARTICLES_URL)
    #     articles = Article.objects.filter(tag="food")
    #     serializer = ArticleSerializer(articles, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_filter_articles_by_date(self):
        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(user, title='Article 1', publication_date=date(2025, 6, 10))
        create_article(user, title='Article 2', publication_date=date(2025, 6, 10))
        create_article(user, title='Article 3', publication_date=date(2025, 5, 10))
        create_article(user, title='Article 4', publication_date=date(2025, 4, 10))

        res =  self.client.get(ARTICLES_LIST_URL, {'publication_date': date(2025, 6, 10)})
        articles = Article.objects.filter(publication_date=date(2025, 6, 10))
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_keyword_search(self):
        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(
            user,
            title='Brain Science',
            abstract="Deep research",
            main_text="Neuroscience is evolving")

        res =  self.client.get(ARTICLES_LIST_URL, {'search': 'neuroscience'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateArticleApiTest(TestCase):
    def setUp(self):
        self.user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_article(self):
        payload = {
            'title': 'Sample title',
            'abstract': 'Sample abstract',
            'publication_date': '2025-01-01'
        }
        res = self.client.post(ARTICLES_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(author=self.user, title=payload['title']).exists())

    def test_update_own_article(self):
        article = create_article(author=self.user, title='Original title')
        url = reverse('article:article-detail', args=[article.id])
        payload = {'title': 'Updated title'}
        res = self.client.patch(url, payload)
        article.refresh_from_db()
        self.assertEqual(article.title, payload['title'])

    def test_update_other_user_article_error(self):
        new_user = create_user(username='other', email='other@example.com', password='pass')
        article = create_article(author=new_user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.patch(url, {'title': 'Hacked'})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_article(self):
        article = create_article(author=self.user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=article.id).exists())

    def test_delete_other_user_article_error(self):
        new_user = create_user(username='other', email='other@example.com', password='pass')
        article = create_article(author=new_user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.filter(id=article.id).exists())

    def test_retrieve_article_detail(self):
        article = create_article(author=self.user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], article.title)
        self.assertEqual(res.data['abstract'], article.abstract)
        self.assertEqual(res.data['publication_date'], str(article.publication_date))
