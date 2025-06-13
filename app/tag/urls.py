"""
URL mappings for the tag API.
"""
from django.urls import path
from tag import views

app_name = 'tag'

urlpatterns = [
    path('', views.TagListCreateView.as_view(), name='tag-list'),
    path('<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
]