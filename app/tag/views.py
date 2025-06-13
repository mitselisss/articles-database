"""
Views for the tag API.
"""
from rest_framework import generics, permissions
from core.models import Tag
from tag.serializers import TagSerializer


class TagListCreateView(generics.ListCreateAPIView):
    """View for listing and creating tags."""
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
