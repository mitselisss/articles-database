"""
Views for the article API.
"""
from rest_framework import generics, permissions
from core.models import Article
from article.serializers import ArticleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from article.permissions import IsAuthor


class ArticleListCreateView(generics.ListCreateAPIView):
    """View for listing and creating articles."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['publication_date', 'author']
    search_fields = ['title', 'abstract', 'main_text']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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