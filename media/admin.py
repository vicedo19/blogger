from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import MediaFile, ImageFile, DocumentFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for MediaFile model.
    """
    list_display = (
        'title',
        'file_type_display',
        'file_size_display',
        'uploaded_by',
        'is_public',
        'created_at'
    )
    list_filter = (
        'file_type',
        'is_public',
        'created_at',
        'updated_at',
        'uploaded_by'
    )
    search_fields = (
        'title',
        'description',
        'uploaded_by__username'
    )
    readonly_fields = (
        'file_size', 
        'mime_type', 
        'download_count', 
        'created_at', 
        'updated_at',
        'file_type_display',
        'file_size_display'
    )
    raw_id_fields = ('uploaded_by',)
    
    fieldsets = (
        ('File Information', {
            'fields': ('title', 'description', 'file', 'file_type', 'is_public')
        }),
        ('Metadata', {
            'fields': ('file_size_display', 'mime_type', 'download_count'),
            'classes': ('collapse',)
        }),
        ('Access Control', {
            'fields': ('uploaded_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('uploaded_by')
    
    def file_type_display(self, obj):
        """Display file type with icon."""
        icons = {
            'image': '🖼️',
            'document': '📄',
            'video': '🎥',
            'audio': '🎵',
            'other': '📎'
        }
        return format_html(
            '{} {}',
            icons.get(obj.file_type, '📎'),
            obj.get_file_type_display()
        )
    file_type_display.short_description = 'Type'
    
    def file_size_display(self, obj):
        """Display file size in human readable format."""
        if obj.file_size:
            if obj.file_size < 1024:
                return f'{obj.file_size} B'
            elif obj.file_size < 1024 * 1024:
                return f'{obj.file_size / 1024:.1f} KB'
            elif obj.file_size < 1024 * 1024 * 1024:
                return f'{obj.file_size / (1024 * 1024):.1f} MB'
            else:
                return f'{obj.file_size / (1024 * 1024 * 1024):.1f} GB'
        return 'Unknown'
    file_size_display.short_description = 'Size'


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for ImageFile model.
    """
    list_display = (
        'title',
        'image_preview',
        'dimensions_display',
        'is_featured',
        'created_at'
    )
    list_filter = (
        'is_featured',
        'media_file__created_at',
        'media_file__uploaded_by'
    )
    search_fields = (
        'media_file__title',
        'alt_text',
        'media_file__uploaded_by__username'
    )
    readonly_fields = (
        'width',
        'height', 
        'image_preview',
        'dimensions_display'
    )
    raw_id_fields = ('media_file',)
    
    fieldsets = (
        ('Image Information', {
            'fields': ('media_file', 'alt_text', 'is_featured')
        }),
        ('Dimensions', {
            'fields': ('width', 'height', 'dimensions_display'),
            'classes': ('collapse',)
        }),
        ('Preview', {
            'fields': ('image_preview', 'thumbnail'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('media_file__uploaded_by')
    
    def title(self, obj):
        """Get title from related MediaFile."""
        return obj.media_file.title
    title.short_description = 'Title'
    
    def created_at(self, obj):
        """Get created_at from related MediaFile."""
        return obj.media_file.created_at
    created_at.short_description = 'Created'
    
    def image_preview(self, obj):
        """Display image preview."""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.thumbnail.url
            )
        elif obj.media_file.file:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.media_file.file.url
            )
        return 'No image'
    image_preview.short_description = 'Preview'
    
    def dimensions_display(self, obj):
        """Display image dimensions."""
        if obj.width and obj.height:
            return f'{obj.width} × {obj.height}'
        return 'Unknown'
    dimensions_display.short_description = 'Dimensions'


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    """
    Admin configuration for DocumentFile model.
    """
    list_display = (
        'title',
        'category',
        'author',
        'page_count',
        'language',
        'created_at'
    )
    list_filter = (
        'category',
        'language',
        'media_file__created_at',
        'media_file__uploaded_by'
    )
    search_fields = (
        'media_file__title',
        'author',
        'media_file__uploaded_by__username'
    )
    readonly_fields = (
        'page_count',
    )
    raw_id_fields = ('media_file',)
    
    fieldsets = (
        ('Document Information', {
            'fields': ('media_file', 'category', 'author', 'language')
        }),
        ('Metadata', {
            'fields': ('page_count',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('media_file__uploaded_by')
    
    def title(self, obj):
        """Get title from related MediaFile."""
        return obj.media_file.title
    title.short_description = 'Title'
    
    def created_at(self, obj):
        """Get created_at from related MediaFile."""
        return obj.media_file.created_at
    created_at.short_description = 'Created'
