"""
Custom permissions for the blog_app API.

This module contains custom permission classes for Django REST Framework
to handle specific authorization requirements for blog functionality.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit it.
    
    - Read permissions are allowed for any request (GET, HEAD, OPTIONS)
    - Write permissions are only allowed to the author of the post
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    
    - Read permissions are allowed for any request (GET, HEAD, OPTIONS)
    - Write permissions are only allowed to the owner of the object
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        # Assumes the model instance has an `owner` attribute.
        return obj.owner == request.user


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission for comment objects.
    
    - Read permissions are allowed for any request
    - Write permissions are only allowed to the comment author
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the comment author
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    
    - Read permissions are allowed for any request
    - Write permissions are only allowed to admin users
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff