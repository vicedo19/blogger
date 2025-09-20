"""
Serializers for the blog_app models.

This module contains Django REST Framework serializers for all blog models,
providing JSON serialization/deserialization for API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Category, Tag, PostStatus


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with basic information."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'post_count']
    
    def get_post_count(self, obj):
        """Return the number of published posts in this category."""
        return obj.posts.filter(status__name='published').count()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']
        read_only_fields = ['id', 'created_at', 'post_count']
    
    def get_post_count(self, obj):
        """Return the number of published posts with this tag."""
        return obj.posts.filter(status__name='published').count()


class PostStatusSerializer(serializers.ModelSerializer):
    """Serializer for PostStatus model."""
    
    class Meta:
        model = PostStatus
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for Post model in list views (minimal fields)."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status = PostStatusSerializer(read_only=True)
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'category', 'tags', 
            'status', 'featured_image', 'reading_time', 'created_at', 
            'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reading_time(self, obj):
        """Calculate estimated reading time based on content length."""
        if obj.content:
            word_count = len(obj.content.split())
            # Average reading speed: 200 words per minute
            reading_time = max(1, word_count // 200)
            return reading_time
        return 1


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for Post model in detail views (all fields)."""
    
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status = PostStatusSerializer(read_only=True)
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt', 'category', 
            'tags', 'status', 'featured_image', 'meta_description', 'reading_time',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def get_reading_time(self, obj):
        """Calculate estimated reading time based on content length."""
        if obj.content:
            word_count = len(obj.content.split())
            # Average reading speed: 200 words per minute
            reading_time = max(1, word_count // 200)
            return reading_time
        return 1


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating Post instances."""
    
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Tag.objects.all(), 
        required=False
    )
    
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt', 'category', 'tags', 
            'status', 'featured_image', 'meta_description'
        ]
    
    def validate_slug(self, value):
        """Ensure slug is unique for the current post."""
        instance = getattr(self, 'instance', None)
        if instance and instance.slug == value:
            return value
        
        if Post.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A post with this slug already exists.")
        return value
    
    def create(self, validated_data):
        """Create a new post instance."""
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags_data)
        return post
    
    def update(self, instance, validated_data):
        """Update an existing post instance."""
        tags_data = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags_data is not None:
            instance.tags.set(tags_data)
        
        return instance