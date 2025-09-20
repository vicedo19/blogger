from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post, Category, Tag


def homepage(request):
    """
    Homepage view that displays published blog posts.
    
    Features:
    - Shows only published posts (status.is_published = True)
    - Orders posts by published_at date (newest first)
    - Includes pagination (10 posts per page)
    - Optimizes database queries with select_related and prefetch_related
    """
    # Get published posts with optimized queries
    posts = Post.objects.filter(
        status__is_published=True,
        published_at__isnull=False
    ).select_related(
        'author', 'category', 'status'
    ).prefetch_related(
        'tags'
    ).order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for sidebar/navigation
    categories = Category.objects.filter(posts__status__is_published=True).distinct()
    popular_tags = Tag.objects.filter(posts__status__is_published=True).distinct()[:10]
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,  # For template compatibility
        'categories': categories,
        'popular_tags': popular_tags,
        'is_homepage': True,
    }
    
    return render(request, 'blog_app/homepage.html', context)
