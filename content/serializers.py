"""
Django REST Framework serializers for the content app.

This module provides serializers for all content models to enable
comprehensive API functionality with proper validation and data transformation.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Category, Tag, PostStatus, Post, 
    PostEngagement, Comment, CommentModeration, CommentReport
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'avatar', 'email_notifications', 
            'show_email_publicly', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 'icon', 
            'color', 'is_active', 'sort_order', 'post_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'post_count']
    
    def get_post_count(self, obj):
        """Get the number of posts in this category."""
        return obj.posts.filter(status__is_published=True).count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    
    class Meta:
        model = Tag
        fields = [
            'id', 'name', 'slug', 'description', 'color', 
            'usage_count', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'usage_count', 'created_at']


class PostStatusSerializer(serializers.ModelSerializer):
    """Serializer for PostStatus model."""
    
    class Meta:
        model = PostStatus
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'color',
            'is_published', 'is_active', 'sort_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post model in list views."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status = PostStatusSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'category', 
            'tags', 'status', 'featured_image', 'is_featured',
            'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'id', 'slug', 'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post model in detail views."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status = PostStatusSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt', 
            'category', 'tags', 'status', 'featured_image', 
            'meta_description', 'meta_keywords', 'is_featured',
            'allow_comments', 'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'id', 'slug', 'view_count', 'like_count', 'comment_count',
            'created_at', 'updated_at'
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts."""
    
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.filter(is_active=True),
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category', 'tags', 'status',
            'featured_image', 'meta_description', 'meta_keywords',
            'is_featured', 'allow_comments'
        ]
    
    def create(self, validated_data):
        """Create a new post."""
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post
    
    def update(self, instance, validated_data):
        """Update an existing post."""
        tags = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags is not None:
            instance.tags.set(tags)
        
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    
    author = UserSerializer(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'parent', 'is_approved',
            'is_flagged', 'like_count', 'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'is_approved', 'is_flagged', 'like_count', 
            'created_at', 'updated_at', 'replies'
        ]
    
    def get_replies(self, obj):
        """Get replies to this comment."""
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_approved=True), 
                many=True, 
                context=self.context
            ).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating comments."""
    
    class Meta:
        model = Comment
        fields = ['post', 'content', 'parent']
    
    def validate_parent(self, value):
        """Validate that parent comment belongs to the same post."""
        if value and value.post != self.initial_data.get('post'):
            raise serializers.ValidationError(
                "Parent comment must belong to the same post."
            )
        return value


class PostEngagementSerializer(serializers.ModelSerializer):
    """Serializer for PostEngagement model."""
    
    user = UserSerializer(read_only=True)
    post = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = PostEngagement
        fields = [
            'id', 'user', 'post', 'liked', 'bookmarked', 
            'shared', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CommentModerationSerializer(serializers.ModelSerializer):
    """Serializer for CommentModeration model."""
    
    comment = CommentSerializer(read_only=True)
    moderator = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentModeration
        fields = [
            'id', 'comment', 'moderator', 'action', 'reason', 
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CommentReportSerializer(serializers.ModelSerializer):
    """Serializer for CommentReport model."""
    
    comment = CommentSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)
    resolved_by = UserSerializer(read_only=True)
    
    class Meta:
        model = CommentReport
        fields = [
            'id', 'comment', 'reporter', 'reason', 'description',
            'status', 'resolved_by', 'resolution_notes',
            'created_at', 'resolved_at'
        ]
        read_only_fields = [
            'id', 'reporter', 'resolved_by', 'created_at', 'resolved_at'
        ]