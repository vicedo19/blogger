"""Comment models for the Django blog application.

This module contains models for comment functionality:
- Comment: User comments on blog posts with threading support
- CommentModeration: Comment moderation and approval workflow
- CommentReport: User reporting system for inappropriate comments
"""

from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    """
    Comment model for user engagement with blog posts.
    
    Features:
    - Threaded comments with parent-child relationships
    - Moderation workflow with approval system
    - Rich content support
    - User association and timestamps
    """
    post = models.ForeignKey('blog_app.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['is_approved']),
        ]
    
    def __str__(self) -> str:
        return f'Comment by {self.author.username} on {self.post.title}'


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
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='moderation_actions')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=MODERATION_ACTIONS)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return f'{self.action.title()} by {self.moderator.username} on comment {self.comment.id}'


class CommentReport(models.Model):
    """
    Comment report model for user-generated reports.
    
    Features:
    - User reporting system
    - Report categorization
    - Status tracking
    """
    REPORT_REASONS = [
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('inappropriate', 'Inappropriate Content'),
        ('off_topic', 'Off Topic'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='resolved_reports'
    )
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['comment', 'reporter']
    
    def __str__(self) -> str:
        return f'Report by {self.reporter.username} on comment {self.comment.id}'
