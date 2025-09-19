"""
Media models for the Django blog application.

This module contains models for file upload and media management:
- MediaFile: General file upload model
- ImageFile: Specialized image file model
- DocumentFile: Document file model
"""

import os
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from PIL import Image


class MediaFile(models.Model):
    """
    Base model for all uploaded files.
    
    Features:
    - File upload with validation
    - File metadata tracking
    - User association
    - File type categorization
    """

    FILE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    FILE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='other')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    mime_type = models.CharField(max_length=100, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    is_public = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['file_type', '-created_at']),
            models.Index(fields=['uploaded_by', '-created_at']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        """Override save to set file metadata."""
        if self.file:
            self.file_size = self.file.size
            # Set file type based on extension
            file_extension = os.path.splitext(self.file.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                self.file_type = 'image'
            elif file_extension in ['.pdf', '.doc', '.docx', '.txt', '.rtf']:
                self.file_type = 'document'
            elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
                self.file_type = 'video'
            elif file_extension in ['.mp3', '.wav', '.flac', '.aac']:
                self.file_type = 'audio'
        super().save(*args, **kwargs)
    
    @property
    def file_size_formatted(self) -> str:
        """Return human-readable file size."""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        elif self.file_size < 1024 * 1024 * 1024:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        else:
            return f"{self.file_size / (1024 * 1024 * 1024):.1f} GB"


class ImageFile(models.Model):
    """
    Specialized model for image files with additional image-specific features.
    
    Features:
    - Image dimension tracking
    - Thumbnail generation
    - Alt text for accessibility
    - Image optimization
    """
    media_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name='image_details')
    alt_text = models.CharField(max_length=200, help_text="Alternative text for accessibility")
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    
    # Image validation
    file_validator = FileExtensionValidator(
        allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']
    )
    
    class Meta:
        verbose_name = "Image File"
        verbose_name_plural = "Image Files"
    
    def __str__(self) -> str:
        return f"Image: {self.media_file.title}"
    
    def save(self, *args, **kwargs):
        """Override save to generate thumbnail and set dimensions."""
        super().save(*args, **kwargs)
        
        if self.media_file.file and not self.thumbnail:
            try:
                # Open the image
                img = Image.open(self.media_file.file.path)
                
                # Set dimensions
                self.width, self.height = img.size
                
                # Generate thumbnail
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                
                # Save thumbnail
                thumb_name = f"thumb_{os.path.basename(self.media_file.file.name)}"
                thumb_path = os.path.join('thumbnails', thumb_name)
                
                # Create thumbnail directory if it doesn't exist
                thumb_dir = os.path.dirname(os.path.join(self.media_file.file.storage.location, thumb_path))
                os.makedirs(thumb_dir, exist_ok=True)
                
                # Save thumbnail
                full_thumb_path = os.path.join(self.media_file.file.storage.location, thumb_path)
                img.save(full_thumb_path)
                self.thumbnail = thumb_path
                
                # Save again with thumbnail and dimensions
                super().save(update_fields=['width', 'height', 'thumbnail'])
                
            except Exception as e:
                # Log error but don't fail the save
                print(f"Error generating thumbnail: {e}")
    
    @property
    def aspect_ratio(self) -> float:
        """Calculate aspect ratio."""
        if self.width and self.height:
            return self.width / self.height
        return 1.0


class DocumentFile(models.Model):
    """
    Specialized model for document files.
    
    Features:
    - Document metadata
    - Page count tracking
    - Document category
    """
    DOCUMENT_CATEGORIES = [
        ('article', 'Article'),
        ('report', 'Report'),
        ('presentation', 'Presentation'),
        ('spreadsheet', 'Spreadsheet'),
        ('other', 'Other'),
    ]
    
    media_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, related_name='document_details')
    category = models.CharField(max_length=20, choices=DOCUMENT_CATEGORIES, default='other')
    page_count = models.PositiveIntegerField(null=True, blank=True)
    author = models.CharField(max_length=200, blank=True)
    language = models.CharField(max_length=10, default='en')
    
    # Document validation
    file_validator = FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
    )
    
    class Meta:
        verbose_name = "Document File"
        verbose_name_plural = "Document Files"
    
    def __str__(self) -> str:
        return f"Document: {self.media_file.title}"
