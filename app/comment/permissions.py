"""
Custom permission for comment author to edit/delete.
"""
from rest_framework import permissions

class IsCommentAuthor(permissions.BasePermission):
    """Custom permission to allow only the author to edit/delete."""

    def has_object_permission(self, request, view, obj):
        print("=== DEBUG PERMISSION CHECK ===")
        print(f"Logged-in user: {request.user.id}")
        print(f"Comment author: {obj.author.id}")
        print(f"Is author? {obj.author == request.user}")
        return obj.author == request.user
