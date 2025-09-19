from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Comment, CommentModeration, CommentReport


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model.
    """
    list_display = (
        'id',
        'author_display',
        'post_title',
        'content_preview',
        'status_display',
        'created_at',
        'is_approved'
    )
    list_filter = (
        'is_approved',
        'created_at',
        'updated_at',
        'post__category'
    )
    search_fields = (
        'content',
        'author__username',
        'author__email',
        'post__title',
        'author_name',
        'author_email'
    )
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('post', 'parent', 'author')
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'parent', 'content')
        }),
        ('Author Information', {
            'fields': ('author', 'author_name', 'author_email', 'author_website')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['approve_comments', 'reject_comments']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'author', 'post', 'parent'
        )
    
    def author_display(self, obj):
        """Display author name with link if registered user."""
        if obj.author:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.author.id,
                obj.author.username
            )
        return obj.author_name or 'Anonymous'
    author_display.short_description = 'Author'
    
    def post_title(self, obj):
        """Display post title with link."""
        return format_html(
            '<a href="/admin/blog_app/post/{}/change/">{}</a>',
            obj.post.id,
            obj.post.title[:50] + ('...' if len(obj.post.title) > 50 else '')
        )
    post_title.short_description = 'Post'
    
    def content_preview(self, obj):
        """Display truncated content."""
        return obj.content[:100] + ('...' if len(obj.content) > 100 else '')
    content_preview.short_description = 'Content'
    
    def status_display(self, obj):
        """Display approval status with color coding."""
        if obj.is_approved:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Approved</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ Not Approved</span>'
        )
    status_display.short_description = 'Status'
    
    def approve_comments(self, request, queryset):
        """Bulk action to approve selected comments."""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} comment(s) were successfully approved.'
        )
    approve_comments.short_description = "Approve selected comments"
    
    def reject_comments(self, request, queryset):
        """Bulk action to reject selected comments."""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated} comment(s) were successfully rejected.'
        )
    reject_comments.short_description = "Reject selected comments"


@admin.register(CommentModeration)
class CommentModerationAdmin(admin.ModelAdmin):
    """
    Admin configuration for CommentModeration model.
    """
    list_display = (
        'comment_preview',
        'moderator',
        'action',
        'reason',
        'created_at'
    )
    list_filter = ('action', 'created_at', 'moderator')
    search_fields = ('comment__content', 'reason', 'moderator__username')
    readonly_fields = ('created_at',)
    raw_id_fields = ('comment', 'moderator')
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'comment', 'moderator'
        )
    
    def comment_preview(self, obj):
        """Display comment content preview."""
        return obj.comment.content[:100] + ('...' if len(obj.comment.content) > 100 else '')
    comment_preview.short_description = 'Comment'


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for CommentReport model.
    """
    list_display = (
        'comment_preview',
        'reporter',
        'reason',
        'status_display',
        'created_at',
        'resolved_by'
    )
    list_filter = (
        'reason',
        'status',
        'created_at',
        'resolved_at'
    )
    search_fields = (
        'comment__content',
        'reporter__username',
        'description',
        'resolved_by__username'
    )
    readonly_fields = ('created_at', 'resolved_at')
    raw_id_fields = ('comment', 'reporter', 'resolved_by')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('comment', 'reporter', 'reason', 'description')
        }),
        ('Resolution', {
            'fields': ('status', 'resolved_by', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['mark_as_resolved', 'mark_as_dismissed']
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'comment', 'reporter', 'resolved_by'
        )
    
    def comment_preview(self, obj):
        """Display comment content preview."""
        return obj.comment.content[:100] + ('...' if len(obj.comment.content) > 100 else '')
    comment_preview.short_description = 'Comment'
    
    def status_display(self, obj):
        """Display status with color coding."""
        colors = {
            'pending': 'orange',
            'resolved': 'green',
            'dismissed': 'gray'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def mark_as_resolved(self, request, queryset):
        """Bulk mark reports as resolved."""
        updated = queryset.update(
            status='resolved',
            resolved_at=timezone.now(),
            resolved_by=request.user
        )
        self.message_user(request, f'{updated} reports marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected reports as resolved'
    
    def mark_as_dismissed(self, request, queryset):
        """Bulk mark reports as dismissed."""
        updated = queryset.update(
            status='dismissed',
            resolved_at=timezone.now(),
            resolved_by=request.user
        )
        self.message_user(request, f'{updated} reports marked as dismissed.')
    mark_as_dismissed.short_description = 'Mark selected reports as dismissed'
