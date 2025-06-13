"""
Custom permission for comment author to edit/delete.
"""
from rest_framework import permissions

class IsCommentAuthor(permissions.BasePermission):
    """Custom permission to allow only the author to edit/delete."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
