"""
Custom filters for blog_app models.

This module defines custom filter classes using django-filter
to provide advanced filtering capabilities for the API endpoints.
"""

import django_filters
from django.db import models
from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Post, Category, Tag, PostStatus


class PostFilter(django_filters.FilterSet):
    """
    Filter class for Post model with advanced filtering options.
    """
    # Text search filters
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    
    # Author filters
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    author_id = django_filters.NumberFilter(field_name='author__id')
    
    # Category and tag filters
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    category_slug = django_filters.CharFilter(field_name='category__slug')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    tag_slugs = django_filters.CharFilter(method='filter_by_tag_slugs')
    
    # Status filters
    status = django_filters.ModelChoiceFilter(queryset=PostStatus.objects.all())
    status_name = django_filters.CharFilter(field_name='status__name', lookup_expr='iexact')
    is_published = django_filters.BooleanFilter(method='filter_published')
    # Note: is_featured field doesn't exist in Post model, removing this filter
    # is_featured = django_filters.BooleanFilter()
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    
    # Date range filters
    created_date = django_filters.DateFromToRangeFilter(field_name='created_at')
    updated_date = django_filters.DateFromToRangeFilter(field_name='updated_at')
    published_date = django_filters.DateFromToRangeFilter(field_name='published_at')
    
    # Numeric filters
    min_reading_time = django_filters.NumberFilter(field_name='reading_time', lookup_expr='gte')
    max_reading_time = django_filters.NumberFilter(field_name='reading_time', lookup_expr='lte')
    reading_time_range = django_filters.RangeFilter(field_name='reading_time')
    
    # Word count filters (if available in model)
    min_word_count = django_filters.NumberFilter(method='filter_min_word_count')
    max_word_count = django_filters.NumberFilter(method='filter_max_word_count')
    
    # Multiple author filter
    authors = django_filters.ModelMultipleChoiceFilter(
        field_name='author',
        queryset=None,  # Will be set in __init__
        to_field_name='id'
    )
    
    # Multiple category filter
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all()
    )
    
    # Content length filters
    has_excerpt = django_filters.BooleanFilter(method='filter_has_excerpt')
    excerpt_length = django_filters.RangeFilter(method='filter_excerpt_length')
    
    class Meta:
        model = Post
        fields = {
            'slug': ['exact', 'icontains'],
            'created_at': ['exact', 'gte', 'lte'],
            'updated_at': ['exact', 'gte', 'lte'],
        }

    def filter_by_tag_slugs(self, queryset, name, value):
        """
        Filter posts by multiple tag slugs (comma-separated).
        """
        if value:
            tag_slugs = [slug.strip() for slug in value.split(',')]
            return queryset.filter(tags__slug__in=tag_slugs).distinct()
        return queryset

    def filter_published(self, queryset, name, value):
        """
        Filter posts by published status.
        """
        if value is True:
            return queryset.filter(status__name='Published')
        elif value is False:
            return queryset.exclude(status__name='Published')
        return queryset

    def filter_min_word_count(self, queryset, name, value):
        """
        Filter posts with at least the specified word count.
        Estimates word count from content length.
        """
        if value is not None:
            # Rough estimate: average 5 characters per word
            min_chars = value * 5
            return queryset.extra(
                where=["LENGTH(content) >= %s"],
                params=[min_chars]
            )
        return queryset

    def filter_max_word_count(self, queryset, name, value):
        """
        Filter posts with at most the specified word count.
        Estimates word count from content length.
        """
        if value is not None:
            # Rough estimate: average 5 characters per word
            max_chars = value * 5
            return queryset.extra(
                where=["LENGTH(content) <= %s"],
                params=[max_chars]
            )
        return queryset

    def filter_has_excerpt(self, queryset, name, value):
        """
        Filter posts that have or don't have an excerpt.
        """
        if value is True:
            return queryset.exclude(excerpt__isnull=True).exclude(excerpt__exact='')
        elif value is False:
            return queryset.filter(Q(excerpt__isnull=True) | Q(excerpt__exact=''))
        return queryset

    def filter_excerpt_length(self, queryset, name, value):
        """
        Filter posts by excerpt length range.
        """
        if value:
            if value.start is not None:
                queryset = queryset.extra(
                    where=["LENGTH(excerpt) >= %s"],
                    params=[value.start]
                )
            if value.stop is not None:
                queryset = queryset.extra(
                    where=["LENGTH(excerpt) <= %s"],
                    params=[value.stop]
                )
        return queryset

    def __init__(self, *args, **kwargs):
        """
        Initialize the filter with dynamic querysets.
        """
        super().__init__(*args, **kwargs)
        # Set the authors queryset dynamically
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.filters['authors'].queryset = User.objects.filter(
            posts__isnull=False
        ).distinct()


class CategoryFilter(django_filters.FilterSet):
    """
    Filter class for Category model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    slug = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Post count filters
    min_posts = django_filters.NumberFilter(method='filter_min_posts')
    max_posts = django_filters.NumberFilter(method='filter_max_posts')
    has_posts = django_filters.BooleanFilter(method='filter_has_posts')

    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']

    def filter_min_posts(self, queryset, name, value):
        """Filter categories with at least the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__gte=value)
        return queryset

    def filter_max_posts(self, queryset, name, value):
        """Filter categories with at most the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__lte=value)
        return queryset

    def filter_has_posts(self, queryset, name, value):
        """Filter categories that have or don't have posts."""
        if value is True:
            return queryset.filter(posts__isnull=False).distinct()
        elif value is False:
            return queryset.filter(posts__isnull=True)
        return queryset


class TagFilter(django_filters.FilterSet):
    """
    Filter class for Tag model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    slug = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Post count filters
    min_posts = django_filters.NumberFilter(method='filter_min_posts')
    max_posts = django_filters.NumberFilter(method='filter_max_posts')
    has_posts = django_filters.BooleanFilter(method='filter_has_posts')

    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def filter_min_posts(self, queryset, name, value):
        """Filter tags with at least the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__gte=value)
        return queryset

    def filter_max_posts(self, queryset, name, value):
        """Filter tags with at most the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__lte=value)
        return queryset

    def filter_has_posts(self, queryset, name, value):
        """Filter tags that have or don't have posts."""
        if value is True:
            return queryset.filter(posts__isnull=False).distinct()
        elif value is False:
            return queryset.filter(posts__isnull=True)
        return queryset


class PostStatusFilter(django_filters.FilterSet):
    """
    Filter class for PostStatus model.
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Post count filters
    min_posts = django_filters.NumberFilter(method='filter_min_posts')
    max_posts = django_filters.NumberFilter(method='filter_max_posts')
    has_posts = django_filters.BooleanFilter(method='filter_has_posts')

    class Meta:
        model = PostStatus
        fields = ['name']

    def filter_min_posts(self, queryset, name, value):
        """Filter statuses with at least the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__gte=value)
        return queryset

    def filter_max_posts(self, queryset, name, value):
        """Filter statuses with at most the specified number of posts."""
        if value is not None:
            return queryset.annotate(
                post_count=models.Count('posts')
            ).filter(post_count__lte=value)
        return queryset

    def filter_has_posts(self, queryset, name, value):
        """Filter statuses that have or don't have posts."""
        if value is True:
            return queryset.filter(posts__isnull=False).distinct()
        elif value is False:
            return queryset.filter(posts__isnull=True)
        return queryset