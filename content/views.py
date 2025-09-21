"""
Django REST Framework views for the content app.

This module provides ViewSets for all content models to enable
comprehensive API functionality with proper permissions and filtering.
"""

from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.utils import timezone

from .models import (
    UserProfile, Category, Tag, PostStatus, Post, 
    PostEngagement, Comment, CommentModeration, CommentReport
)
from .serializers import (
    UserSerializer, UserProfileSerializer, CategorySerializer,
    TagSerializer, PostStatusSerializer, PostListSerializer,
    PostDetailSerializer, PostCreateUpdateSerializer,
    CommentSerializer, CommentCreateSerializer,
    PostEngagementSerializer, CommentModerationSerializer,
    CommentReportSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model - read-only operations."""
    
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['-date_joined']


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model."""
    
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'bio']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # Only show profiles that allow public email display
            queryset = queryset.filter(show_email_publicly=True)
        return queryset
    
    def perform_create(self, serializer):
        """Set the user when creating a profile."""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure users can only update their own profile."""
        if serializer.instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only update your own profile.")
        serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model."""
    
    queryset = Category.objects.filter(is_active=True).prefetch_related('posts')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['parent', 'is_active']
    ordering_fields = ['name', 'sort_order', 'created_at']
    ordering = ['sort_order', 'name']
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all posts in this category."""
        category = self.get_object()
        posts = Post.objects.filter(
            category=category,
            status__is_published=True
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for Tag model."""
    
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'usage_count', 'created_at']
    ordering = ['-usage_count', 'name']
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all posts with this tag."""
        tag = self.get_object()
        posts = Post.objects.filter(
            tags=tag,
            status__is_published=True
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for PostStatus model - read-only operations."""
    
    queryset = PostStatus.objects.filter(is_active=True)
    serializer_class = PostStatusSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['sort_order', 'name']
    ordering = ['sort_order']


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model."""
    
    queryset = Post.objects.select_related(
        'author', 'category', 'status'
    ).prefetch_related('tags').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'content', 'excerpt']
    filterset_fields = ['category', 'tags', 'status', 'is_featured', 'author']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'view_count', 'like_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        else:
            return PostDetailSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        
        if not self.request.user.is_authenticated:
            # Anonymous users only see published posts
            queryset = queryset.filter(status__is_published=True)
        elif not self.request.user.is_staff:
            # Regular users see published posts and their own posts
            queryset = queryset.filter(
                Q(status__is_published=True) | Q(author=self.request.user)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author when creating a post."""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure users can only update their own posts (unless staff)."""
        if not self.request.user.is_staff and serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only update your own posts.")
        serializer.save()
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving a post."""
        instance = self.get_object()
        
        # Increment view count
        Post.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        
        # Refresh instance to get updated view count
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like or unlike a post."""
        post = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        engagement, created = PostEngagement.objects.get_or_create(
            user=user, post=post
        )
        
        if engagement.liked:
            engagement.liked = False
            engagement.save()
            Post.objects.filter(pk=post.pk).update(like_count=F('like_count') - 1)
            message = 'Post unliked'
        else:
            engagement.liked = True
            engagement.save()
            Post.objects.filter(pk=post.pk).update(like_count=F('like_count') + 1)
            message = 'Post liked'
        
        return Response({'message': message})
    
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Bookmark or unbookmark a post."""
        post = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        engagement, created = PostEngagement.objects.get_or_create(
            user=user, post=post
        )
        
        engagement.bookmarked = not engagement.bookmarked
        engagement.save()
        
        message = 'Post bookmarked' if engagement.bookmarked else 'Post unbookmarked'
        return Response({'message': message})
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for this post."""
        post = self.get_object()
        comments = Comment.objects.filter(
            post=post,
            is_approved=True,
            parent=None  # Only top-level comments
        ).select_related('author').prefetch_related('replies')
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model."""
    
    queryset = Comment.objects.select_related('author', 'post').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['post', 'is_approved', 'is_flagged']
    ordering_fields = ['created_at', 'updated_at', 'like_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create']:
            return CommentCreateSerializer
        else:
            return CommentSerializer
    
    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            # Non-staff users only see approved comments
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author when creating a comment."""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure users can only update their own comments (unless staff)."""
        if not self.request.user.is_staff and serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only update your own comments.")
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a comment (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Staff permission required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        
        # Update post comment count
        Post.objects.filter(pk=comment.post.pk).update(
            comment_count=F('comment_count') + 1
        )
        
        return Response({'message': 'Comment approved'})
    
    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        """Flag a comment for moderation."""
        comment = self.get_object()
        comment.is_flagged = True
        comment.save()
        
        return Response({'message': 'Comment flagged for moderation'})


class PostEngagementViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for PostEngagement model - read-only operations."""
    
    queryset = PostEngagement.objects.select_related('user', 'post').all()
    serializer_class = PostEngagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['liked', 'bookmarked', 'shared']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Users can only see their own engagements."""
        return super().get_queryset().filter(user=self.request.user)


class CommentModerationViewSet(viewsets.ModelViewSet):
    """ViewSet for CommentModeration model (staff only)."""
    
    queryset = CommentModeration.objects.select_related('comment', 'moderator').all()
    serializer_class = CommentModerationSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['action', 'comment']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the moderator when creating a moderation record."""
        serializer.save(moderator=self.request.user)


class CommentReportViewSet(viewsets.ModelViewSet):
    """ViewSet for CommentReport model."""
    
    queryset = CommentReport.objects.select_related(
        'comment', 'reporter', 'resolved_by'
    ).all()
    serializer_class = CommentReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'reason']
    ordering_fields = ['created_at', 'resolved_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter based on user permissions."""
        queryset = super().get_queryset()
        
        if self.request.user.is_staff:
            # Staff can see all reports
            return queryset
        else:
            # Regular users can only see their own reports
            return queryset.filter(reporter=self.request.user)
    
    def perform_create(self, serializer):
        """Set the reporter when creating a report."""
        serializer.save(reporter=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a comment report (staff only)."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Staff permission required'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        report = self.get_object()
        report.status = 'resolved'
        report.resolved_by = request.user
        report.resolved_at = timezone.now()
        report.resolution_notes = request.data.get('resolution_notes', '')
        report.save()
        
        return Response({'message': 'Report resolved'})
