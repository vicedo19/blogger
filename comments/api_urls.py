"""
API URL configuration for comments app.

This module defines the URL patterns for the comments API endpoints
using Django REST Framework routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CommentViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]