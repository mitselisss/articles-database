"""
Tests for the article API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Article, Tag
from article.serializers import ArticleSerializer
from datetime import date


ARTICLES_LIST_URL = reverse('article:article-list')
ARTICLE_DOWNLOAD_URL = reverse('article:article-download')


def create_user(**params):
    return get_user_model().objects.create(**params)


def create_article(authors, **params):
    default = {
        'title': 'Sample Title',
        'abstract': 'Sample Abstract',
        'publication_date': date.today()
    }
    default.update(params)
    article = Article.objects.create(**default)
    if isinstance(authors, list):
        article.authors.set(authors)
    else:
        article.authors.set([authors])

    return article


class PublicArticleApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_create(self):
        """Test unauthorized creation returns error."""
        payload = {
            'title': 'Unauthorized',
            'abstract': 'Should not work',
            'publication_date': '2025-01-01'
        }
        res = self.client.post(ARTICLES_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_articles(self):
        """Test everyone can list articls."""
        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(user, title='Article 1')
        create_article(user, title='Article 2')

        res = self.client.get(ARTICLES_LIST_URL)
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_articles_by_authors(self):
        """Test filtering articles by author(s)."""
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

        res = self.client.get(ARTICLES_LIST_URL, {'authors': user1.id})
        articles = Article.objects.filter(authors=user1)
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_articles_by_tag(self):
        """Test filtering articles by tag(s)."""
        tag1 = Tag.objects.create(name='test1')
        tag2 = Tag.objects.create(name='test2')

        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )

        article1 = create_article(authors=user, title='Sample title1')
        article2 = create_article(authors=user, title='Sample title2')
        article1.tags.add(tag1)
        article2.tags.add(tag2)

        res = self.client.get(ARTICLES_LIST_URL, {'tags': tag1.id})
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]['title'], 'Sample title1')

    def test_filter_articles_by_date(self):
        """Test filtering articles by date."""
        user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass1234'
        )
        create_article(
            user,
            title='Article 1',
            publication_date=date(2025, 6, 10)
        )
        create_article(
            user,
            title='Article 1',
            publication_date=date(2025, 6, 10)
        )
        create_article(
            user,
            title='Article 1',
            publication_date=date(2025, 5, 10)
        )
        create_article(
            user,
            title='Article 1',
            publication_date=date(2025, 4, 10)
        )

        res = self.client.get(
            ARTICLES_LIST_URL, {'publication_date': date(2025, 6, 10)})
        articles = Article.objects.filter(publication_date=date(2025, 6, 10))
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_keyword_search(self):
        """Test searching for a keyword."""
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

        res = self.client.get(ARTICLES_LIST_URL, {'search': 'neuroscience'})

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
        """Test authorized creation of article."""
        payload = {
            'title': 'Sample title',
            'abstract': 'Sample abstract',
            'publication_date': '2025-01-01'
        }
        res = self.client.post(ARTICLES_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(
            authors=self.user, title=payload['title']).exists())

    def test_update_own_article(self):
        """Test authorized update of article."""
        article = create_article(authors=self.user, title='Original title')
        url = reverse('article:article-detail', args=[article.id])
        payload = {'title': 'Updated title'}
        res = self.client.patch(url, payload)
        article.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(article.title, payload['title'])

    def test_update_other_user_article_error(self):
        """Test unauthorized updated of article returns error."""
        new_user = create_user(
            username='other',
            email='other@example.com',
            password='pass'
        )
        article = create_article(authors=new_user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.patch(url, {'title': 'Hacked'})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_article(self):
        """Test authorized deletion of article."""
        article = create_article(authors=self.user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(id=article.id).exists())

    def test_delete_other_user_article_error(self):
        """Test unauthorized deletion of article returns error."""
        new_user = create_user(
            username='other',
            email='other@example.com',
            password='pass'
        )
        article = create_article(authors=new_user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Article.objects.filter(id=article.id).exists())

    def test_retrieve_article_detail(self):
        """Test authorized retrieve of article return the correct details."""
        article = create_article(authors=self.user)
        url = reverse('article:article-detail', args=[article.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], article.title)
        self.assertEqual(res.data['abstract'], article.abstract)
        self.assertEqual(
            res.data['publication_date'], str(article.publication_date))


class ArticleDownloadCSVTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='testuser',
            email='test@example.com',
            password='pass123')
        self.article = create_article(authors=self.user)

    def test_download_csv_returns_csv_file(self):
        """Test downloading article as CSV."""
        res = self.client.get(ARTICLE_DOWNLOAD_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res['Content-Type'], 'text/csv')
        self.assertIn(
            'attachment; filename="articles.csv"',
            res['Content-Disposition']
        )
        self.assertIn('Sample Title', res.content.decode())
