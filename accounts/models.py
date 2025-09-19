"""
Account models for the Django blog application.

This module contains simplified models for basic user account functionality:
- UserProfile: Essential user profile information
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Simplified user profile model with essential information only.
    
    Features:
    - One-to-one relationship with Django User model
    - Basic profile information (bio, avatar)
    - Timestamps for tracking
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Profile picture")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create UserProfile when User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save UserProfile when User is saved.
    """
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
