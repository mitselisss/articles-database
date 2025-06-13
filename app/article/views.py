"""
Views for the article API.
"""
from rest_framework import generics, permissions
from core.models import Article
from article.serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from article.permissions import IsAuthor
import csv
from django.http import HttpResponse


class ArticleListCreateView(generics.ListCreateAPIView):
    """View for listing and creating articles."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['publication_date', 'authors', 'tags']
    search_fields = ['title', 'abstract', 'main_text']

    def perform_create(self, serializer):
        article = serializer.save()
        if self.request.user not in article.authors.all():
            article.authors.add(self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting an article."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.AllowAny()]


class ArticleDownloadCSVView(generics.ListAPIView):
    """View for returning a csv with filtered articles."""
    queryset = Article.objects.all().order_by('id')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['publication_date', 'authors', 'tags', 'id']
    search_fields = ['title', 'abstract', 'main_text']

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="articles.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID',
            'Title',
            'Abstract',
            'Publication Date',
            'Authors',
            'Tags'
        ])

        for article in queryset:
            writer.writerow([
                article.id,
                article.title,
                article.abstract,
                article.publication_date,
                [author.username for author in article.authors.all()],
                [tag.name for tag in article.tags.all()],
            ])

        return response
