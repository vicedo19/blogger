from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag, PostStatus


@admin.register(PostStatus)
class PostStatusAdmin(admin.ModelAdmin):
    """
    Admin configuration for PostStatus model.
    """
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ('name', 'slug', 'description', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fields = ('name', 'slug', 'description', 'created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for Tag model.
    """
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    fields = ('name', 'slug', 'created_at')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model.
    """
    list_display = (
        'title',
        'author',
        'category',
        'status',
        'is_published',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'status', 
        'category', 
        'tags', 
        'created_at', 
        'published_at',
        'updated_at'
    )
    search_fields = ('title', 'content', 'excerpt', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug', 'created_at', 'updated_at', 'published_at')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'featured_image')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Publication', {
            'fields': ('status', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related and prefetch_related."""
        return super().get_queryset(request).select_related(
            'author', 'category', 'status'
        ).prefetch_related('tags')
    
    def is_published(self, obj):
        """Display publication status with colored indicator."""
        if obj.is_published:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Published</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Not Published</span>'
        )
    is_published.short_description = 'Published Status'
    
    def save_model(self, request, obj, form, change):
        """Set author to current user if not set."""
        if not change:  # Only for new posts
            obj.author = request.user
        super().save_model(request, obj, form, change)
