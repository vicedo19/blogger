"""
Admin configurations for the content app models.

This module provides comprehensive admin interfaces for all content-related models:
- UserProfile: User profile management
- Category: Hierarchical category management
- Tag: Tag management with usage tracking
- PostStatus: Dynamic status management
- Post: Rich post management with inline editing
- PostEngagement: Engagement tracking
- Comment: Comment moderation and management
- CommentModeration: Moderation action tracking
- CommentReport: Report management and resolution
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    UserProfile, Category, Tag, PostStatus, Post, PostEngagement,
    Comment, CommentModeration, CommentReport
)


# =============================================================================
# USER PROFILE ADMIN
# =============================================================================

class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile in User admin."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = (
        'bio', 'avatar', 'website',
        ('email_notifications', 'show_email_publicly')
    )


class UserAdmin(BaseUserAdmin):
    """Extended User admin with UserProfile inline."""
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = (
        'user', 'display_name', 'email_notifications', 
        'show_email_publicly', 'created_at'
    )
    list_filter = ('email_notifications', 'show_email_publicly', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'show_email_publicly')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_name(self, obj):
        """Display the user's display name."""
        return obj.display_name
    display_name.short_description = 'Display Name'


# =============================================================================
# CONTENT ORGANIZATION ADMIN
# =============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    list_display = (
        'name', 'parent', 'post_count', 'is_active', 
        'sort_order', 'created_at'
    )
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('sort_order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'sort_order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def post_count(self, obj):
        """Display the number of posts in this category."""
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""
    list_display = (
        'name', 'usage_count', 'is_active', 'color_display', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('usage_count', 'created_at')
    ordering = ('-usage_count', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('color', 'is_active')
        }),
        ('Statistics', {
            'fields': ('usage_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        """Display color as a colored box."""
        if obj.color:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
                obj.color
            )
        return '-'
    color_display.short_description = 'Color'


@admin.register(PostStatus)
class PostStatusAdmin(admin.ModelAdmin):
    """Admin interface for PostStatus model."""
    list_display = (
        'name', 'is_published', 'is_active', 'sort_order', 
        'color_display', 'post_count'
    )
    list_filter = ('is_published', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('sort_order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('icon', 'color', 'sort_order')
        }),
        ('Publishing Settings', {
            'fields': ('is_published', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def color_display(self, obj):
        """Display color as a colored box."""
        if obj.color:
            return format_html(
                '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
                obj.color
            )
        return '-'
    color_display.short_description = 'Color'
    
    def post_count(self, obj):
        """Display the number of posts with this status."""
        return obj.posts.count()
    post_count.short_description = 'Posts'


# =============================================================================
# POST ADMIN
# =============================================================================

class PostEngagementInline(admin.TabularInline):
    """Inline admin for PostEngagement."""
    model = PostEngagement
    extra = 0
    readonly_fields = ('user', 'engagement_type', 'created_at')
    can_delete = False


class CommentInline(admin.TabularInline):
    """Inline admin for Comments."""
    model = Comment
    extra = 0
    readonly_fields = ('author', 'created_at', 'is_approved')
    fields = ('author', 'content', 'is_approved', 'created_at')
    can_delete = False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""
    list_display = (
        'title', 'author', 'status', 'category', 'is_featured',
        'view_count', 'like_count', 'comment_count', 'created_at'
    )
    list_filter = (
        'status', 'category', 'is_featured', 'allow_comments',
        'created_at', 'published_at'
    )
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'view_count', 'like_count', 'comment_count',
        'created_at', 'updated_at', 'reading_time'
    )
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
    inlines = [CommentInline, PostEngagementInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'status')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_featured', 'allow_comments', 'published_at')
        }),
        ('Statistics', {
            'fields': ('view_count', 'like_count', 'comment_count', 'reading_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def reading_time(self, obj):
        """Display estimated reading time."""
        return f"{obj.reading_time} min"
    reading_time.short_description = 'Reading Time'


@admin.register(PostEngagement)
class PostEngagementAdmin(admin.ModelAdmin):
    """Admin interface for PostEngagement model."""
    list_display = ('user', 'post', 'engagement_type', 'created_at')
    list_filter = ('engagement_type', 'created_at')
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


# =============================================================================
# COMMENT ADMIN
# =============================================================================

class CommentModerationInline(admin.TabularInline):
    """Inline admin for CommentModeration."""
    model = CommentModeration
    extra = 0
    readonly_fields = ('created_at',)


class CommentReportInline(admin.TabularInline):
    """Inline admin for CommentReport."""
    model = CommentReport
    extra = 0
    readonly_fields = ('reporter', 'reason', 'created_at')
    fields = ('reporter', 'reason', 'status', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    list_display = (
        'author', 'post', 'is_approved', 'is_flagged',
        'like_count', 'reply_count', 'created_at'
    )
    list_filter = (
        'is_approved', 'is_flagged', 'created_at', 'post__category'
    )
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('like_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [CommentModerationInline, CommentReportInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('post', 'author', 'content', 'parent')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_flagged')
        }),
        ('Statistics', {
            'fields': ('like_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def reply_count(self, obj):
        """Display the number of replies to this comment."""
        return obj.replies.count()
    reply_count.short_description = 'Replies'
    
    actions = ['approve_comments', 'flag_comments', 'unflag_comments']
    
    def approve_comments(self, request, queryset):
        """Bulk approve comments."""
        updated = queryset.update(is_approved=True, is_flagged=False)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def flag_comments(self, request, queryset):
        """Bulk flag comments."""
        updated = queryset.update(is_flagged=True)
        self.message_user(request, f'{updated} comments were flagged.')
    flag_comments.short_description = 'Flag selected comments'
    
    def unflag_comments(self, request, queryset):
        """Bulk unflag comments."""
        updated = queryset.update(is_flagged=False)
        self.message_user(request, f'{updated} comments were unflagged.')
    unflag_comments.short_description = 'Unflag selected comments'


@admin.register(CommentModeration)
class CommentModerationAdmin(admin.ModelAdmin):
    """Admin interface for CommentModeration model."""
    list_display = ('comment', 'moderator', 'action', 'created_at')
    list_filter = ('action', 'created_at', 'moderator')
    search_fields = ('comment__content', 'moderator__username', 'reason')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Moderation Action', {
            'fields': ('comment', 'moderator', 'action')
        }),
        ('Details', {
            'fields': ('reason', 'notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    """Admin interface for CommentReport model."""
    list_display = (
        'comment', 'reporter', 'reason', 'status', 
        'created_at', 'resolved_by'
    )
    list_filter = ('reason', 'status', 'created_at', 'resolved_at')
    search_fields = ('comment__content', 'reporter__username', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('comment', 'reporter', 'reason', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Resolution', {
            'fields': ('resolved_at', 'resolved_by', 'resolution_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_reviewed', 'mark_as_resolved', 'mark_as_dismissed']
    
    def mark_as_reviewed(self, request, queryset):
        """Mark reports as under review."""
        updated = queryset.update(status='under_review')
        self.message_user(request, f'{updated} reports marked as under review.')
    mark_as_reviewed.short_description = 'Mark as under review'
    
    def mark_as_resolved(self, request, queryset):
        """Mark reports as resolved."""
        from django.utils import timezone
        updated = queryset.update(
            status='resolved', 
            resolved_at=timezone.now(),
            resolved_by=request.user
        )
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_as_resolved.short_description = 'Mark as resolved'
    
    def mark_as_dismissed(self, request, queryset):
        """Mark reports as dismissed."""
        from django.utils import timezone
        updated = queryset.update(
            status='dismissed',
            resolved_at=timezone.now(),
            resolved_by=request.user
        )
        self.message_user(request, f'{updated} reports marked as dismissed.')
    mark_as_dismissed.short_description = 'Mark as dismissed'


# =============================================================================
# ADMIN SITE CUSTOMIZATION
# =============================================================================

admin.site.site_header = 'Blog Content Administration'
admin.site.site_title = 'Blog Admin'
admin.site.index_title = 'Content Management'
