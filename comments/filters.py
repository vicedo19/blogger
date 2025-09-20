"""
Custom filters for comments app models.

This module defines custom filter classes using django-filter
to provide advanced filtering capabilities for the comment API endpoints.
"""

import django_filters
from django.db import models
from .models import Comment


class CommentFilter(django_filters.FilterSet):
    """
    Filter class for Comment model with advanced filtering options.
    """
    # Text search filters
    content = django_filters.CharFilter(lookup_expr='icontains')
    content_length_min = django_filters.NumberFilter(method='filter_content_length_min')
    content_length_max = django_filters.NumberFilter(method='filter_content_length_max')
    
    # Author filters
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    author_id = django_filters.NumberFilter(field_name='author__id')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    authors = django_filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=None,  # Will be set dynamically in __init__
        to_field_name='id'
    )
    
    # Post filters
    post = django_filters.NumberFilter(field_name='post__id')
    post_slug = django_filters.CharFilter(field_name='post__slug')
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    posts = django_filters.ModelMultipleChoiceFilter(
        field_name='post',
        queryset=None,  # Will be set dynamically in __init__
        to_field_name='id'
    )
    post_category = django_filters.CharFilter(field_name='post__category__slug')
    post_status = django_filters.CharFilter(field_name='post__status__name')
    
    # Parent comment filters
    parent = django_filters.NumberFilter(field_name='parent__id')
    is_reply = django_filters.BooleanFilter(method='filter_is_reply')
    is_top_level = django_filters.BooleanFilter(method='filter_is_top_level')
    thread_depth = django_filters.NumberFilter(method='filter_thread_depth')
    
    # Approval status filters
    is_approved = django_filters.BooleanFilter()
    approval_status = django_filters.ChoiceFilter(
        method='filter_approval_status',
        choices=[
            ('approved', 'Approved'),
            ('pending', 'Pending'),
            ('rejected', 'Rejected'),
        ]
    )
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    # Date range filters
    created_date = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_date = django_filters.DateFromToRangeFilter(field_name='updated_at')
    
    # Time-based filters
    created_today = django_filters.BooleanFilter(method='filter_created_today')
    created_this_week = django_filters.BooleanFilter(method='filter_created_this_week')
    created_this_month = django_filters.BooleanFilter(method='filter_created_this_month')
    
    # Reply count filters
    min_replies = django_filters.NumberFilter(method='filter_min_replies')
    max_replies = django_filters.NumberFilter(method='filter_max_replies')
    has_replies = django_filters.BooleanFilter(method='filter_has_replies')
    
    # Content quality filters
    has_long_content = django_filters.BooleanFilter(method='filter_has_long_content')
    has_short_content = django_filters.BooleanFilter(method='filter_has_short_content')

    class Meta:
        model = Comment
        fields = {
            'created_at': ['exact', 'gte', 'lte'],
            'updated_at': ['exact', 'gte', 'lte'],
            'is_approved': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the filter with dynamic querysets.
        """
        super().__init__(*args, **kwargs)
        # Set the authors queryset dynamically
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.filters['authors'].queryset = User.objects.filter(
            comments__isnull=False
        ).distinct()
        
        # Set the posts queryset dynamically
        from blog_app.models import Post
        self.filters['posts'].queryset = Post.objects.filter(
            comments__isnull=False
        ).distinct()

    def filter_is_reply(self, queryset, name, value):
        """
        Filter comments that are replies (have a parent comment).
        """
        if value is True:
            return queryset.filter(parent__isnull=False)
        elif value is False:
            return queryset.filter(parent__isnull=True)
        return queryset

    def filter_is_top_level(self, queryset, name, value):
        """
        Filter top-level comments (no parent comment).
        """
        if value is True:
            return queryset.filter(parent__isnull=True)
        elif value is False:
            return queryset.filter(parent__isnull=False)
        return queryset

    def filter_approval_status(self, queryset, name, value):
        """
        Filter comments by approval status.
        """
        if value == 'approved':
            return queryset.filter(is_approved=True)
        elif value == 'pending':
            return queryset.filter(is_approved=False)
        elif value == 'rejected':
            # Assuming rejected comments are those that were explicitly disapproved
            # This might need adjustment based on your business logic
            return queryset.filter(is_approved=False)
        return queryset

    def filter_min_replies(self, queryset, name, value):
        """
        Filter comments with at least the specified number of replies.
        """
        if value is not None:
            return queryset.annotate(
                reply_count=models.Count('replies')
            ).filter(reply_count__gte=value)
        return queryset

    def filter_max_replies(self, queryset, name, value):
        """
        Filter comments with at most the specified number of replies.
        """
        if value is not None:
            return queryset.annotate(
                reply_count=models.Count('replies')
            ).filter(reply_count__lte=value)
        return queryset

    def filter_has_replies(self, queryset, name, value):
        """
        Filter comments that have or don't have replies.
        """
        if value is True:
            return queryset.filter(replies__isnull=False).distinct()
        elif value is False:
            return queryset.filter(replies__isnull=True)
        return queryset

    def filter_content_length_min(self, queryset, name, value):
        """
        Filter comments with at least the specified content length.
        """
        if value is not None:
            return queryset.extra(
                where=["LENGTH(content) >= %s"],
                params=[value]
            )
        return queryset

    def filter_content_length_max(self, queryset, name, value):
        """
        Filter comments with at most the specified content length.
        """
        if value is not None:
            return queryset.extra(
                where=["LENGTH(content) <= %s"],
                params=[value]
            )
        return queryset

    def filter_thread_depth(self, queryset, name, value):
        """
        Filter comments by thread depth (0 = top-level, 1 = first reply, etc.).
        """
        if value == 0:
            return queryset.filter(parent__isnull=True)
        elif value == 1:
            return queryset.filter(parent__isnull=False, parent__parent__isnull=True)
        elif value >= 2:
            # For deeper levels, we need to count the parent chain
            # This is a simplified approach - for exact depth matching,
            # you might need a more complex query or denormalized depth field
            return queryset.filter(parent__parent__isnull=False)
        return queryset

    def filter_created_today(self, queryset, name, value):
        """
        Filter comments created today.
        """
        if value is True:
            from django.utils import timezone
            today = timezone.now().date()
            return queryset.filter(created_at__date=today)
        return queryset

    def filter_created_this_week(self, queryset, name, value):
        """
        Filter comments created this week.
        """
        if value is True:
            from django.utils import timezone
            from datetime import timedelta
            week_ago = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=week_ago)
        return queryset

    def filter_created_this_month(self, queryset, name, value):
        """
        Filter comments created this month.
        """
        if value is True:
            from django.utils import timezone
            now = timezone.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return queryset.filter(created_at__gte=month_start)
        return queryset

    def filter_has_long_content(self, queryset, name, value):
        """
        Filter comments with long content (>200 characters).
        """
        if value is True:
            return queryset.extra(
                where=["LENGTH(content) > %s"],
                params=[200]
            )
        elif value is False:
            return queryset.extra(
                where=["LENGTH(content) <= %s"],
                params=[200]
            )
        return queryset

    def filter_has_short_content(self, queryset, name, value):
        """
        Filter comments with short content (<=50 characters).
        """
        if value is True:
            return queryset.extra(
                where=["LENGTH(content) <= %s"],
                params=[50]
            )
        elif value is False:
            return queryset.extra(
                where=["LENGTH(content) > %s"],
                params=[50]
            )
        return queryset