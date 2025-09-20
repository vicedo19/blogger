"""API views for blog_app using Django REST Framework.

This module contains ViewSets for handling CRUD operations
on blog models through REST API endpoints.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone

from .models import Post, Category, Tag, PostStatus
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer, PostStatusSerializer
)
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly
from .filters import PostFilter, CategoryFilter, TagFilter, PostStatusFilter


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model with comprehensive CRUD operations.
    
    Provides endpoints for managing blog categories with filtering and search.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all published posts in this category."""
        category = self.get_object()
        posts = Post.objects.filter(
            category=category,
            status__name='published'
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Tag model with comprehensive CRUD operations.
    
    Provides endpoints for managing blog tags with filtering and search.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all published posts with this tag."""
        tag = self.get_object()
        posts = Post.objects.filter(
            tags=tag,
            status__name='published'
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PostStatus model with comprehensive CRUD operations.
    
    Provides endpoints for managing post statuses with filtering and search.
    """
    queryset = PostStatus.objects.all()
    serializer_class = PostStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostStatusFilter
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model with comprehensive CRUD operations.
    
    Provides endpoints for managing blog posts with advanced filtering,
    search capabilities, and proper permissions.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'excerpt', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return posts with optimized queries and proper filtering.
        """
        return Post.objects.select_related(
            'author', 'category', 'status'
        ).prefetch_related('tags').all()

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        """
        Set the author to the current user when creating a post.
        """
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """Get all posts by the current user."""
        posts = Post.objects.filter(
            author=request.user
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def drafts(self, request):
        """Get all draft posts by the current user."""
        drafts = Post.objects.filter(
            author=request.user,
            status__name='draft'
        ).select_related('author', 'category', 'status').prefetch_related('tags')
        
        serializer = PostListSerializer(drafts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, pk=None):
        """Publish a draft post."""
        post = self.get_object()
        
        # Check if user is the author
        if post.author != request.user:
            return Response(
                {'error': 'You can only publish your own posts.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if post is in draft status
        if post.status.name != 'draft':
            return Response(
                {'error': 'Only draft posts can be published.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status to published
        published_status = PostStatus.objects.get(name='published')
        post.status = published_status
        post.published_at = timezone.now()
        post.save()
        
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unpublish(self, request, pk=None):
        """Unpublish a published post (move to draft)."""
        post = self.get_object()
        
        # Check if user is the author
        if post.author != request.user:
            return Response(
                {'error': 'You can only unpublish your own posts.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if post is published
        if post.status.name != 'published':
            return Response(
                {'error': 'Only published posts can be unpublished.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status to draft
        draft_status = PostStatus.objects.get(name='draft')
        post.status = draft_status
        post.published_at = None
        post.save()
        
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts (posts with featured images)."""
        featured_posts = Post.objects.filter(
            status__name='published',
            featured_image__isnull=False
        ).exclude(featured_image='').select_related(
            'author', 'category', 'status'
        ).prefetch_related('tags')[:10]
        
        serializer = PostListSerializer(featured_posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular posts (most commented)."""
        popular_posts = Post.objects.filter(
            status__name='published'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-comment_count').select_related(
            'author', 'category', 'status'
        ).prefetch_related('tags')[:10]
        
        serializer = PostListSerializer(popular_posts, many=True, context={'request': request})
        return Response(serializer.data)