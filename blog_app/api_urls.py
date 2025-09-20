"""
API URL configuration for blog_app.

This module defines the URL patterns for the blog API endpoints
using Django REST Framework routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PostViewSet, CategoryViewSet, TagViewSet, PostStatusViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'post-statuses', PostStatusViewSet, basename='poststatus')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]