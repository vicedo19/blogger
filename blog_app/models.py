"""
Core blog models for the Django blog application.

This module contains the main models for the blog functionality:
- Category: Organizes posts into categories
- Tag: Flexible labeling system for posts
- Post: Main content entity with publishing workflow
- PostStatus: Dynamic post status management
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PostStatus(models.Model):
    """
    Dynamic post status management for flexible publishing workflow.
    
    Features:
    - Admin-manageable status options
    - Workflow customization
    - Status-based permissions
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI display")
    is_published = models.BooleanField(default=False, help_text="Whether posts with this status are publicly visible")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Post Status"
        verbose_name_plural = "Post Statuses"
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'sort_order']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """
    Category model for organizing blog posts.
    
    Provides hierarchical organization of posts with unique names and slugs.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """
    Tag model for flexible labeling of blog posts.
    
    Provides many-to-many relationship with posts for flexible categorization.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Post model representing the main blog content entity.
    
    Features:
    - Dynamic publishing workflow with flexible status management
    - SEO optimization with meta descriptions and slugs
    - Content organization with categories and tags
    - Featured images for visual appeal
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status = models.ForeignKey(
        PostStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        """
        Override save method to set published_at when status changes to published
        and set default status if none provided.
        """
        # Set default status if none provided
        if not self.status:
            try:
                default_status = PostStatus.objects.filter(
                    slug='draft',
                    is_active=True
                ).first()
                if default_status:
                    self.status = default_status
            except PostStatus.DoesNotExist:
                pass
        
        # Set published_at when status changes to a published status
        if self.status and self.status.is_published and not self.published_at:
            self.published_at = timezone.now()
        elif self.status and not self.status.is_published:
            self.published_at = None
            
        super().save(*args, **kwargs)
    
    @property
    def is_published(self) -> bool:
        """Check if the post is in a published status."""
        return self.status and self.status.is_published
