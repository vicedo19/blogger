"""
Content models for the Django blog application.

This module contains consolidated models for all content-related functionality:
- UserProfile: User profile information and settings
- Category: Content organization by categories
- Tag: Flexible labeling system for content
- PostStatus: Dynamic post status management
- Post: Main content entity with publishing workflow
- PostEngagement: User engagement tracking (likes, bookmarks, etc.)
- Comment: User comments with threading and moderation
- CommentModeration: Comment moderation workflow
- CommentReport: User reporting system for comments
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from typing import Optional


# =============================================================================
# USER-RELATED MODELS
# =============================================================================

class UserProfile(models.Model):
    """
    User profile model with essential information and preferences.
    
    Features:
    - One-to-one relationship with Django User model
    - Profile information (bio, avatar, social links)
    - User preferences and settings
    - Timestamps for tracking
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='content_profile')
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Profile picture")
    
    # User preferences
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    show_email_publicly = models.BooleanField(default=False, help_text="Display email address on profile")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"
    
    @property
    def display_name(self) -> str:
        """Return the user's display name (full name or username)."""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to automatically create UserProfile when User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save UserProfile when User is saved."""
    if hasattr(instance, 'content_profile'):
        instance.content_profile.save()


# =============================================================================
# CONTENT ORGANIZATION MODELS
# =============================================================================

class Category(models.Model):
    """
    Category model for organizing content into hierarchical categories.
    
    Features:
    - Unique category names and slugs
    - SEO-friendly descriptions
    - Hierarchical structure support
    - Timestamps for tracking
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI display")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'sort_order']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """
    Tag model for flexible content labeling and categorization.
    
    Features:
    - Unique tag names and slugs
    - Usage tracking
    - Color coding for UI
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI display")
    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['-usage_count']),
        ]
    
    def __str__(self) -> str:
        return self.name


class PostStatus(models.Model):
    """
    Dynamic post status management for flexible publishing workflow.
    
    Features:
    - Admin-manageable status options
    - Workflow customization
    - Status-based permissions
    - UI customization (icons, colors)
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


# =============================================================================
# MAIN CONTENT MODELS
# =============================================================================

class Post(models.Model):
    """
    Main post model for blog content with comprehensive features.
    
    Features:
    - Rich content with metadata
    - Category and tag organization
    - Dynamic status management
    - SEO optimization
    - Publishing workflow
    - Media support
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief description for previews and SEO")
    
    # Organization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Status and publishing
    status = models.ForeignKey(PostStatus, on_delete=models.SET_NULL, null=True, blank=True,related_name='posts')
    
    # Media
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True, help_text="Main image for the post")
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma-separated)")
    
    # Engagement metrics
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    
    # Publishing
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['-published_at']),
        ]
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        """Custom save method to handle publishing logic."""
        # Auto-set published_at when status changes to published
        if self.status and self.status.is_published and not self.published_at:
            self.published_at = timezone.now()
        elif self.status and not self.status.is_published:
            self.published_at = None
        
        super().save(*args, **kwargs)
    
    @property
    def is_published(self) -> bool:
        """Check if the post is published."""
        return (
            self.status and 
            self.status.is_published and 
            self.published_at and 
            self.published_at <= timezone.now()
        )
    
    @property
    def reading_time(self) -> int:
        """Estimate reading time in minutes."""
        word_count = len(self.content.split())
        return max(1, word_count // 200)  # Assume 200 words per minute


# =============================================================================
# ENGAGEMENT MODELS
# =============================================================================

class PostEngagement(models.Model):
    """
    Track user engagement with posts (likes, bookmarks, shares, etc.).
    
    Features:
    - Multiple engagement types
    - User-post relationship tracking
    - Timestamps for analytics
    """
    ENGAGEMENT_TYPES = [
        ('like', 'Like'),
        ('bookmark', 'Bookmark'),
        ('share', 'Share'),
        ('view', 'View'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='engagements')
    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post', 'engagement_type']
        indexes = [
            models.Index(fields=['post', 'engagement_type']),
            models.Index(fields=['user', 'engagement_type']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self) -> str:
        return f"{self.user.username} {self.engagement_type}d {self.post.title}"


# =============================================================================
# COMMENT MODELS
# =============================================================================

class Comment(models.Model):
    """
    Comment model for user engagement with blog posts.
    
    Features:
    - Threaded comments with parent-child relationships
    - Moderation workflow with approval system
    - Rich content support
    - User association and timestamps
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_comments')
    content = models.TextField()
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)
    
    # Engagement
    like_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['is_approved']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self) -> str:
        return f'Comment by {self.author.username} on {self.post.title}'
    
    @property
    def is_reply(self) -> bool:
        """Check if this comment is a reply to another comment."""
        return self.parent is not None
    
    def get_replies(self):
        """Get all approved replies to this comment."""
        return self.replies.filter(is_approved=True).order_by('created_at')


class CommentModeration(models.Model):
    """
    Comment moderation model for tracking moderation actions.
    
    Features:
    - Track moderation actions and reasons
    - Moderator attribution
    - Action timestamps
    """
    MODERATION_ACTIONS = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged'),
        ('spam', 'Marked as Spam'),
        ('edited', 'Edited'),
    ]
    
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name='moderation_actions'
    )
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_moderation_actions')
    action = models.CharField(max_length=20, choices=MODERATION_ACTIONS)
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Internal moderation notes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['comment']),
            models.Index(fields=['moderator']),
            models.Index(fields=['action']),
        ]
    
    def __str__(self) -> str:
        return f'{self.action.title()} by {self.moderator.username} on comment {self.comment.id}'


class CommentReport(models.Model):
    """
    Comment report model for user-generated reports.
    
    Features:
    - User reporting system
    - Report categorization
    - Status tracking
    - Resolution workflow
    """
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('off_topic', 'Off Topic'),
        ('misinformation', 'Misinformation'),
        ('copyright', 'Copyright Violation'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_reports')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(
        blank=True,
        help_text="Additional details about the report"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    # Resolution tracking
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='content_resolved_reports'
    )
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['comment', 'reporter']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['reason']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self) -> str:
        return f'Report by {self.reporter.username} on comment {self.comment.id}'
