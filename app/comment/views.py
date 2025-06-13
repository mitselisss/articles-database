"""
Views for the comment API.
"""
from rest_framework import generics, permissions
from core.models import Comment
from comment.serializers import CommentSerializer
from comment.permissions import IsCommentAuthor


class CommentListCreateView(generics.ListCreateAPIView):
    """View for listing and creating tags."""
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsCommentAuthor()]
        return [permissions.AllowAny()]
