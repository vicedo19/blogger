"""
Account models for the Django blog application.

This module contains models for user account functionality:
- UserProfile: Extended user information and profile data
- UserPreferences: User-specific settings and preferences
- UserActivity: Track user engagement and activity
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile model with additional information.
    
    Features:
    - One-to-one relationship with Django User model
    - Profile customization (bio, avatar, social links)
    - Professional information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_username = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self) -> str:
        return f'{self.user.username} Profile'


class UserPreferences(models.Model):
    """
    User preferences model for customizable settings.
    
    Features:
    - Email notification preferences
    - Privacy settings
    - Display preferences
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    email_notifications = models.BooleanField(default=True)
    email_on_comment = models.BooleanField(default=True)
    email_on_reply = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=False)
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('friends', 'Friends Only'),
        ],
        default='public'
    )
    show_email = models.BooleanField(default=False)
    show_real_name = models.BooleanField(default=True)
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto'),
        ],
        default='auto'
    )
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Preferences"
        verbose_name_plural = "User Preferences"
    
    def __str__(self) -> str:
        return f'{self.user.username} Preferences'


class UserActivity(models.Model):
    """
    User activity tracking model.
    
    Features:
    - Track user engagement metrics
    - Login history
    - Content interaction statistics
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('post_created', 'Post Created'),
        ('post_updated', 'Post Updated'),
        ('comment_created', 'Comment Created'),
        ('profile_updated', 'Profile Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.get_activity_type_display()}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create UserProfile and UserPreferences when User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)
        UserPreferences.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save UserProfile and UserPreferences when User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'preferences'):
        instance.preferences.save()
