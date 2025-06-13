"""
URL mappings for the article API.
"""
from django.urls import path
from article import views
app_name = 'article'

urlpatterns = [
    path(
        '',
        views.ArticleListCreateView.as_view(),
        name='article-list'
    ),
    path(
        '<int:pk>/',
        views.ArticleDetailView.as_view(),
        name='article-detail'
    ),
    path(
        'download/',
        views.ArticleDownloadCSVView.as_view(),
        name='article-download'
    ),
]
