"""
URL mappings for the comment API.
"""
from django.urls import path
from comment import views

app_name = 'comment'

urlpatterns = [
    path('', views.CommentListCreateView.as_view(), name='comment-list'),
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]