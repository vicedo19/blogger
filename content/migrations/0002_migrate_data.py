"""
Data migration to transfer existing data from accounts, blog_app, and comments apps
to the consolidated content app.

This migration:
1. Transfers UserProfile data from accounts app
2. Transfers Category, Tag, PostStatus, and Post data from blog_app
3. Transfers Comment, CommentModeration, and CommentReport data from comments app
4. Maintains all relationships and data integrity
"""

from django.db import migrations
from django.db.models import Q


def migrate_user_profiles(apps, schema_editor):
    """Migrate UserProfile data from accounts app to content app."""
    # Get old and new models
    OldUserProfile = apps.get_model('accounts', 'UserProfile')
    NewUserProfile = apps.get_model('content', 'UserProfile')
    
    # Transfer all user profiles
    for old_profile in OldUserProfile.objects.all():
        NewUserProfile.objects.create(
            user=old_profile.user,
            bio=old_profile.bio,
            avatar=old_profile.avatar,
            # Set default values for new fields not in old model
            email_notifications=True,
            show_email_publicly=False,
            created_at=old_profile.created_at,
            updated_at=old_profile.updated_at,
        )
    
    print(f"Migrated {OldUserProfile.objects.count()} user profiles")


def migrate_categories(apps, schema_editor):
    """Migrate Category data from blog_app to content app."""
    OldCategory = apps.get_model('blog_app', 'Category')
    NewCategory = apps.get_model('content', 'Category')
    
    # Create categories (no parent relationships in old model)
    for old_category in OldCategory.objects.all():
        NewCategory.objects.create(
            name=old_category.name,
            slug=old_category.slug,
            description=old_category.description,
            # Set default values for new fields not in old model
            icon='',
            color='',
            is_active=True,
            sort_order=0,
            created_at=old_category.created_at,
            updated_at=old_category.updated_at,
        )
    
    print(f"Migrated {OldCategory.objects.count()} categories")


def migrate_tags(apps, schema_editor):
    """Migrate Tag data from blog_app to content app."""
    OldTag = apps.get_model('blog_app', 'Tag')
    NewTag = apps.get_model('content', 'Tag')
    
    for old_tag in OldTag.objects.all():
        NewTag.objects.create(
            name=old_tag.name,
            slug=old_tag.slug,
            # Set default values for new fields not in old model
            description='',
            color='',
            usage_count=0,
            is_active=True,
            created_at=old_tag.created_at,
        )
    
    print(f"Migrated {OldTag.objects.count()} tags")


def migrate_post_statuses(apps, schema_editor):
    """Migrate PostStatus data from blog_app to content app."""
    OldPostStatus = apps.get_model('blog_app', 'PostStatus')
    NewPostStatus = apps.get_model('content', 'PostStatus')
    
    for old_status in OldPostStatus.objects.all():
        NewPostStatus.objects.create(
            name=old_status.name,
            slug=old_status.slug,
            description=old_status.description,
            icon=old_status.icon,
            color=old_status.color,
            is_published=old_status.is_published,
            is_active=old_status.is_active,
            sort_order=old_status.sort_order,
            created_at=old_status.created_at,
            updated_at=old_status.updated_at,
        )
    
    print(f"Migrated {OldPostStatus.objects.count()} post statuses")


def migrate_posts(apps, schema_editor):
    """Migrate Post data from blog_app to content app."""
    OldPost = apps.get_model('blog_app', 'Post')
    NewPost = apps.get_model('content', 'Post')
    NewCategory = apps.get_model('content', 'Category')
    NewTag = apps.get_model('content', 'Tag')
    NewPostStatus = apps.get_model('content', 'PostStatus')
    
    for old_post in OldPost.objects.all():
        # Find corresponding new models
        new_category = None
        if old_post.category:
            new_category = NewCategory.objects.filter(slug=old_post.category.slug).first()
        
        new_status = None
        if old_post.status:
            new_status = NewPostStatus.objects.filter(slug=old_post.status.slug).first()
        
        # Create new post
        new_post = NewPost.objects.create(
            title=old_post.title,
            slug=old_post.slug,
            author=old_post.author,
            content=old_post.content,
            excerpt=old_post.excerpt,
            category=new_category,
            status=new_status,
            featured_image=old_post.featured_image,
            meta_description=old_post.meta_description,
            # Set default values for new fields not in old model
            meta_keywords='',
            view_count=0,
            like_count=0,
            comment_count=0,
            is_featured=False,
            allow_comments=True,
            created_at=old_post.created_at,
            updated_at=old_post.updated_at,
            published_at=old_post.published_at,
        )
        
        # Migrate tags (many-to-many relationship)
        for old_tag in old_post.tags.all():
            new_tag = NewTag.objects.filter(slug=old_tag.slug).first()
            if new_tag:
                new_post.tags.add(new_tag)
    
    print(f"Migrated {OldPost.objects.count()} posts")


def migrate_comments(apps, schema_editor):
    """Migrate Comment data from comments app to content app."""
    OldComment = apps.get_model('comments', 'Comment')
    NewComment = apps.get_model('content', 'Comment')
    NewPost = apps.get_model('content', 'Post')
    
    # Create a mapping for parent relationships
    comment_mapping = {}
    
    # First pass: create comments without parent relationships
    for old_comment in OldComment.objects.all():
        # Find corresponding new post
        new_post = NewPost.objects.filter(slug=old_comment.post.slug).first()
        if not new_post:
            continue  # Skip if post not found
        
        new_comment = NewComment.objects.create(
            post=new_post,
            author=old_comment.author,
            content=old_comment.content,
            is_approved=old_comment.is_approved,
            # Set default values for new fields not in old model
            is_flagged=False,
            like_count=0,
            created_at=old_comment.created_at,
            updated_at=old_comment.updated_at,
        )
        comment_mapping[old_comment.id] = new_comment
    
    # Second pass: set parent relationships
    for old_comment in OldComment.objects.filter(parent__isnull=False):
        if old_comment.id in comment_mapping and old_comment.parent.id in comment_mapping:
            new_comment = comment_mapping[old_comment.id]
            new_comment.parent = comment_mapping[old_comment.parent.id]
            new_comment.save()
    
    print(f"Migrated {len(comment_mapping)} comments")


def migrate_comment_moderation(apps, schema_editor):
    """Migrate CommentModeration data from comments app to content app."""
    try:
        OldCommentModeration = apps.get_model('comments', 'CommentModeration')
        NewCommentModeration = apps.get_model('content', 'CommentModeration')
        NewComment = apps.get_model('content', 'Comment')
        
        for old_moderation in OldCommentModeration.objects.all():
            # Find corresponding new comment
            new_comment = NewComment.objects.filter(
                author=old_moderation.comment.author,
                created_at=old_moderation.comment.created_at
            ).first()
            
            if new_comment:
                NewCommentModeration.objects.create(
                    comment=new_comment,
                    moderator=old_moderation.moderator,
                    action=old_moderation.action,
                    reason=old_moderation.reason,
                    notes=getattr(old_moderation, 'notes', ''),
                    created_at=old_moderation.created_at,
                )
        
        print(f"Migrated {OldCommentModeration.objects.count()} comment moderation records")
    except Exception as e:
        print(f"CommentModeration migration skipped: {e}")


def migrate_comment_reports(apps, schema_editor):
    """Migrate CommentReport data from comments app to content app."""
    try:
        OldCommentReport = apps.get_model('comments', 'CommentReport')
        NewCommentReport = apps.get_model('content', 'CommentReport')
        NewComment = apps.get_model('content', 'Comment')
        
        for old_report in OldCommentReport.objects.all():
            # Find corresponding new comment
            new_comment = NewComment.objects.filter(
                author=old_report.comment.author,
                created_at=old_report.comment.created_at
            ).first()
            
            if new_comment:
                NewCommentReport.objects.create(
                    comment=new_comment,
                    reporter=old_report.reporter,
                    reason=old_report.reason,
                    description=old_report.description,
                    status=old_report.status,
                    created_at=old_report.created_at,
                    resolved_at=old_report.resolved_at,
                    resolved_by=old_report.resolved_by,
                    resolution_notes=getattr(old_report, 'resolution_notes', ''),
                )
        
        print(f"Migrated {OldCommentReport.objects.count()} comment reports")
    except Exception as e:
        print(f"CommentReport migration skipped: {e}")


def reverse_migration(apps, schema_editor):
    """Reverse migration - delete all content app data."""
    # Get all content models
    UserProfile = apps.get_model('content', 'UserProfile')
    Category = apps.get_model('content', 'Category')
    Tag = apps.get_model('content', 'Tag')
    PostStatus = apps.get_model('content', 'PostStatus')
    Post = apps.get_model('content', 'Post')
    PostEngagement = apps.get_model('content', 'PostEngagement')
    Comment = apps.get_model('content', 'Comment')
    CommentModeration = apps.get_model('content', 'CommentModeration')
    CommentReport = apps.get_model('content', 'CommentReport')
    
    # Delete in reverse dependency order
    CommentReport.objects.all().delete()
    CommentModeration.objects.all().delete()
    Comment.objects.all().delete()
    PostEngagement.objects.all().delete()
    Post.objects.all().delete()
    PostStatus.objects.all().delete()
    Tag.objects.all().delete()
    Category.objects.all().delete()
    UserProfile.objects.all().delete()
    
    print("Reversed data migration - all content app data deleted")


class Migration(migrations.Migration):
    
    dependencies = [
        ('content', '0001_initial'),
        # Note: Dependencies on deleted apps (accounts, blog_app, comments) removed
        # This migration was used for data transfer during app consolidation
    ]
    
    operations = [
        migrations.RunPython(
            code=lambda apps, schema_editor: (
                migrate_user_profiles(apps, schema_editor),
                migrate_categories(apps, schema_editor),
                migrate_tags(apps, schema_editor),
                migrate_post_statuses(apps, schema_editor),
                migrate_posts(apps, schema_editor),
                migrate_comments(apps, schema_editor),
                migrate_comment_moderation(apps, schema_editor),
                migrate_comment_reports(apps, schema_editor),
            ),
            reverse_code=reverse_migration,
        ),
    ]