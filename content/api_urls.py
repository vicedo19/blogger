"""
API URL configuration for the content app.

This module defines the REST API endpoints using Django REST Framework
routers to automatically generate URL patterns for ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, UserProfileViewSet, CategoryViewSet, TagViewSet,
    PostStatusViewSet, PostViewSet, PostEngagementViewSet,
    CommentViewSet, CommentModerationViewSet, CommentReportViewSet
)

# Create a router and register our ViewSets with it
router = DefaultRouter()

# User management endpoints
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

# Content organization endpoints
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'post-statuses', PostStatusViewSet, basename='poststatus')

# Blog post endpoints
router.register(r'posts', PostViewSet, basename='post')

# Engagement endpoints
router.register(r'engagements', PostEngagementViewSet, basename='postengagement')

# Comment system endpoints
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'comment-moderations', CommentModerationViewSet, basename='commentmoderation')
router.register(r'comment-reports', CommentReportViewSet, basename='commentreport')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]