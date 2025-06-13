"""
Custom permission for article author to edit/delete.
"""
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Custom permission to allow only the author to edit/delete."""

    def has_object_permission(self, request, view, obj):
        return request.user in obj.authors.all()
