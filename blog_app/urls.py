"""
URL configuration for blog_app.

This module defines URL patterns for the blog application views.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
]