"""
API views for comments app using Django REST Framework.

This module contains ViewSets for handling CRUD operations
on comment models through REST API endpoints.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Comment
from .serializers import (
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
)
from blog_app.permissions import IsCommentAuthorOrReadOnly
from .filters import CommentFilter


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model with comprehensive CRUD operations.
    
    Provides endpoints for managing comments with nested replies support,
    moderation capabilities, and advanced filtering.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['content', 'author__username', 'post__title']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return comments with optimized queries and proper filtering.
        """
        return Comment.objects.select_related(
            'author', 'post', 'parent'
        ).prefetch_related('replies').all()

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['create']:
            return CommentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a comment.
        """
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get all replies to a specific comment."""
        comment = self.get_object()
        replies = comment.replies.filter(is_approved=True).select_related('author')
        
        serializer = CommentSerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reply(self, request, pk=None):
        """Reply to a comment."""
        parent_comment = self.get_object()
        
        # Create reply data
        reply_data = request.data.copy()
        reply_data['parent'] = parent_comment.id
        reply_data['post'] = parent_comment.post.id
        
        serializer = CommentCreateSerializer(data=reply_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_comments(self, request):
        """Get all comments by the current user."""
        comments = Comment.objects.filter(
            author=request.user
        ).select_related('author', 'post').prefetch_related('replies')
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def pending_approval(self, request):
        """Get all comments pending approval (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can view pending comments.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comments = Comment.objects.filter(
            is_approved=False
        ).select_related('author', 'post')
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve a comment (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff members can approve comments.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject a comment (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to reject comments.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment = self.get_object()
        comment.is_approved = False
        comment.save()
        
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)