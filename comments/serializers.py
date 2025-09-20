"""
Serializers for the comments app models.

This module contains Django REST Framework serializers for comment-related models,
providing JSON serialization/deserialization for API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment


class CommentAuthorSerializer(serializers.ModelSerializer):
    """Serializer for comment author information."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model with nested author information."""
    
    author = CommentAuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'parent', 'is_approved',
            'replies', 'reply_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'is_approved']
    
    def get_replies(self, obj):
        """Get direct replies to this comment."""
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_approved=True), 
                many=True, 
                context=self.context
            ).data
        return []
    
    def get_reply_count(self, obj):
        """Get the count of approved replies."""
        return obj.replies.filter(is_approved=True).count()


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new comments."""
    
    class Meta:
        model = Comment
        fields = ['post', 'content', 'parent']
    
    def validate_parent(self, value):
        """Validate that parent comment belongs to the same post."""
        if value and hasattr(self.initial_data, 'get'):
            post_id = self.initial_data.get('post')
            if value.post.id != int(post_id):
                raise serializers.ValidationError(
                    "Parent comment must belong to the same post."
                )
        return value
    
    def create(self, validated_data):
        """Create a new comment with the current user as author."""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing comments."""
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def validate(self, attrs):
        """Ensure only the comment author can update the comment."""
        if self.instance.author != self.context['request'].user:
            raise serializers.ValidationError(
                "You can only edit your own comments."
            )
        return attrs