"""
Comprehensive tests for the content app models.

This module provides thorough testing for all content-related models:
- UserProfile: User profile functionality and validation
- Category: Hierarchical category management
- Tag: Tag functionality and usage tracking
- PostStatus: Dynamic status management
- Post: Blog post creation, validation, and methods
- PostEngagement: User engagement tracking
- Comment: Comment system with threading and moderation
- CommentModeration: Moderation action tracking
- CommentReport: Report management and resolution
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta

from .models import (
    UserProfile, Category, Tag, PostStatus, Post, PostEngagement,
    Comment, CommentModeration, CommentReport
)


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test UserProfile is created automatically when User is created."""
        # UserProfile should be created via signal
        self.assertTrue(hasattr(self.user, 'userprofile'))
        profile = self.user.userprofile
        self.assertEqual(profile.user, self.user)
        self.assertIsNotNone(profile.created_at)
    
    def test_display_name_property(self):
        """Test display_name property returns correct value."""
        profile = self.user.userprofile
        
        # Test with no first/last name
        self.assertEqual(profile.display_name, 'testuser')
        
        # Test with first name only
        self.user.first_name = 'John'
        self.user.save()
        self.assertEqual(profile.display_name, 'John')
        
        # Test with full name
        self.user.last_name = 'Doe'
        self.user.save()
        self.assertEqual(profile.display_name, 'John Doe')
    
    def test_user_profile_str_method(self):
        """Test UserProfile string representation."""
        profile = self.user.userprofile
        self.assertEqual(str(profile), 'testuser')
    
    def test_user_profile_fields(self):
        """Test UserProfile field validation and storage."""
        profile = self.user.userprofile
        profile.bio = 'Test bio'
        profile.website = 'https://example.com'
        profile.twitter_handle = '@testuser'
        profile.github_username = 'testuser'
        profile.linkedin_profile = 'https://linkedin.com/in/testuser'
        profile.email_notifications = False
        profile.show_email_publicly = True
        profile.save()
        
        # Refresh from database
        profile.refresh_from_db()
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.website, 'https://example.com')
        self.assertEqual(profile.twitter_handle, '@testuser')
        self.assertEqual(profile.github_username, 'testuser')
        self.assertEqual(profile.linkedin_profile, 'https://linkedin.com/in/testuser')
        self.assertFalse(profile.email_notifications)
        self.assertTrue(profile.show_email_publicly)


class CategoryModelTest(TestCase):
    """Test cases for Category model."""
    
    def setUp(self):
        """Set up test data."""
        self.parent_category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Technology related posts'
        )
    
    def test_category_creation(self):
        """Test Category creation and basic fields."""
        category = Category.objects.create(
            name='Web Development',
            slug='web-development',
            description='Web development tutorials'
        )
        
        self.assertEqual(category.name, 'Web Development')
        self.assertEqual(category.slug, 'web-development')
        self.assertEqual(category.description, 'Web development tutorials')
        self.assertTrue(category.is_active)
        self.assertEqual(category.sort_order, 0)
        self.assertIsNotNone(category.created_at)
    
    def test_category_hierarchy(self):
        """Test category parent-child relationships."""
        child_category = Category.objects.create(
            name='Django',
            slug='django',
            parent=self.parent_category
        )
        
        self.assertEqual(child_category.parent, self.parent_category)
        self.assertIn(child_category, self.parent_category.children.all())
    
    def test_category_str_method(self):
        """Test Category string representation."""
        self.assertEqual(str(self.parent_category), 'Technology')
    
    def test_category_unique_slug(self):
        """Test category slug uniqueness."""
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='Another Tech',
                slug='technology'  # Same slug as parent_category
            )
    
    def test_category_ordering(self):
        """Test category ordering by sort_order and name."""
        cat1 = Category.objects.create(name='Z Category', sort_order=1)
        cat2 = Category.objects.create(name='A Category', sort_order=2)
        cat3 = Category.objects.create(name='B Category', sort_order=1)
        
        categories = Category.objects.all()
        # Should be ordered by sort_order, then name
        expected_order = [self.parent_category, cat3, cat1, cat2]
        self.assertEqual(list(categories), expected_order)


class TagModelTest(TestCase):
    """Test cases for Tag model."""
    
    def test_tag_creation(self):
        """Test Tag creation and basic fields."""
        tag = Tag.objects.create(
            name='Python',
            slug='python',
            description='Python programming language',
            color='#3776ab'
        )
        
        self.assertEqual(tag.name, 'Python')
        self.assertEqual(tag.slug, 'python')
        self.assertEqual(tag.description, 'Python programming language')
        self.assertEqual(tag.color, '#3776ab')
        self.assertTrue(tag.is_active)
        self.assertEqual(tag.usage_count, 0)
        self.assertIsNotNone(tag.created_at)
    
    def test_tag_str_method(self):
        """Test Tag string representation."""
        tag = Tag.objects.create(name='Django', slug='django')
        self.assertEqual(str(tag), 'Django')
    
    def test_tag_unique_slug(self):
        """Test tag slug uniqueness."""
        Tag.objects.create(name='Python', slug='python')
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='Python Lang', slug='python')
    
    def test_tag_ordering(self):
        """Test tag ordering by usage_count and name."""
        tag1 = Tag.objects.create(name='Z Tag', usage_count=5)
        tag2 = Tag.objects.create(name='A Tag', usage_count=10)
        tag3 = Tag.objects.create(name='B Tag', usage_count=5)
        
        tags = Tag.objects.all()
        # Should be ordered by -usage_count, then name
        expected_order = [tag2, tag3, tag1]
        self.assertEqual(list(tags), expected_order)


class PostStatusModelTest(TestCase):
    """Test cases for PostStatus model."""
    
    def test_post_status_creation(self):
        """Test PostStatus creation and basic fields."""
        status = PostStatus.objects.create(
            name='Published',
            slug='published',
            description='Post is published and visible',
            is_published=True,
            color='#28a745'
        )
        
        self.assertEqual(status.name, 'Published')
        self.assertEqual(status.slug, 'published')
        self.assertEqual(status.description, 'Post is published and visible')
        self.assertTrue(status.is_published)
        self.assertEqual(status.color, '#28a745')
        self.assertTrue(status.is_active)
        self.assertEqual(status.sort_order, 0)
    
    def test_post_status_str_method(self):
        """Test PostStatus string representation."""
        status = PostStatus.objects.create(name='Draft', slug='draft')
        self.assertEqual(str(status), 'Draft')
    
    def test_post_status_ordering(self):
        """Test PostStatus ordering by sort_order and name."""
        status1 = PostStatus.objects.create(name='Z Status', sort_order=1)
        status2 = PostStatus.objects.create(name='A Status', sort_order=2)
        status3 = PostStatus.objects.create(name='B Status', sort_order=1)
        
        statuses = PostStatus.objects.all()
        expected_order = [status3, status1, status2]
        self.assertEqual(list(statuses), expected_order)


class PostModelTest(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.tag1 = Tag.objects.create(name='Python', slug='python')
        self.tag2 = Tag.objects.create(name='Django', slug='django')
    
    def test_post_creation(self):
        """Test Post creation and basic fields."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is test content.',
            excerpt='Test excerpt',
            category=self.category,
            status=self.status
        )
        
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.slug, 'test-post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, 'This is test content.')
        self.assertEqual(post.excerpt, 'Test excerpt')
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.status, self.status)
        self.assertTrue(post.allow_comments)
        self.assertFalse(post.is_featured)
        self.assertEqual(post.view_count, 0)
        self.assertEqual(post.like_count, 0)
        self.assertEqual(post.comment_count, 0)
    
    def test_post_str_method(self):
        """Test Post string representation."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content',
            category=self.category,
            status=self.status
        )
        self.assertEqual(str(post), 'Test Post')
    
    def test_post_reading_time_property(self):
        """Test reading time calculation."""
        # Create post with known word count
        content = ' '.join(['word'] * 250)  # 250 words
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content=content,
            category=self.category,
            status=self.status
        )
        
        # Should be approximately 1 minute (250 words / 200 wpm)
        self.assertEqual(post.reading_time, 1)
    
    def test_post_get_absolute_url(self):
        """Test get_absolute_url method."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content',
            category=self.category,
            status=self.status
        )
        expected_url = f'/posts/{post.slug}/'
        self.assertEqual(post.get_absolute_url(), expected_url)
    
    def test_post_tags_relationship(self):
        """Test many-to-many relationship with tags."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content',
            category=self.category,
            status=self.status
        )
        
        post.tags.add(self.tag1, self.tag2)
        self.assertEqual(post.tags.count(), 2)
        self.assertIn(self.tag1, post.tags.all())
        self.assertIn(self.tag2, post.tags.all())
    
    def test_post_unique_slug(self):
        """Test post slug uniqueness."""
        Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content',
            category=self.category,
            status=self.status
        )
        
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                title='Another Test Post',
                slug='test-post',  # Same slug
                author=self.user,
                content='Content',
                category=self.category,
                status=self.status
            )


class PostEngagementModelTest(TestCase):
    """Test cases for PostEngagement model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123'
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Content',
            category=self.category,
            status=self.status
        )
    
    def test_post_engagement_creation(self):
        """Test PostEngagement creation."""
        engagement = PostEngagement.objects.create(
            user=self.user,
            post=self.post,
            engagement_type='like'
        )
        
        self.assertEqual(engagement.user, self.user)
        self.assertEqual(engagement.post, self.post)
        self.assertEqual(engagement.engagement_type, 'like')
        self.assertIsNotNone(engagement.created_at)
    
    def test_post_engagement_str_method(self):
        """Test PostEngagement string representation."""
        engagement = PostEngagement.objects.create(
            user=self.user,
            post=self.post,
            engagement_type='like'
        )
        expected_str = f'{self.user.username} liked {self.post.title}'
        self.assertEqual(str(engagement), expected_str)
    
    def test_post_engagement_unique_constraint(self):
        """Test unique constraint on user, post, engagement_type."""
        PostEngagement.objects.create(
            user=self.user,
            post=self.post,
            engagement_type='like'
        )
        
        # Should not be able to create duplicate engagement
        with self.assertRaises(IntegrityError):
            PostEngagement.objects.create(
                user=self.user,
                post=self.post,
                engagement_type='like'
            )


class CommentModelTest(TestCase):
    """Test cases for Comment model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Content',
            category=self.category,
            status=self.status
        )
    
    def test_comment_creation(self):
        """Test Comment creation."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertFalse(comment.is_approved)  # Default is False
        self.assertFalse(comment.is_flagged)
        self.assertEqual(comment.like_count, 0)
        self.assertIsNone(comment.parent)
    
    def test_comment_str_method(self):
        """Test Comment string representation."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='This is a test comment.'
        )
        expected_str = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(comment), expected_str)
    
    def test_comment_threading(self):
        """Test comment parent-child relationships."""
        parent_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Parent comment'
        )
        
        child_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Child comment',
            parent=parent_comment
        )
        
        self.assertEqual(child_comment.parent, parent_comment)
        self.assertIn(child_comment, parent_comment.replies.all())
    
    def test_comment_get_absolute_url(self):
        """Test get_absolute_url method."""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
        expected_url = f'/posts/{self.post.slug}/#comment-{comment.id}'
        self.assertEqual(comment.get_absolute_url(), expected_url)


class CommentModerationModelTest(TestCase):
    """Test cases for CommentModeration model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            email='moderator@example.com',
            password='testpass123'
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Content',
            category=self.category,
            status=self.status
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_comment_moderation_creation(self):
        """Test CommentModeration creation."""
        moderation = CommentModeration.objects.create(
            comment=self.comment,
            moderator=self.moderator,
            action='approved',
            reason='Comment is appropriate'
        )
        
        self.assertEqual(moderation.comment, self.comment)
        self.assertEqual(moderation.moderator, self.moderator)
        self.assertEqual(moderation.action, 'approved')
        self.assertEqual(moderation.reason, 'Comment is appropriate')
        self.assertIsNotNone(moderation.created_at)
    
    def test_comment_moderation_str_method(self):
        """Test CommentModeration string representation."""
        moderation = CommentModeration.objects.create(
            comment=self.comment,
            moderator=self.moderator,
            action='approved'
        )
        expected_str = f'{moderation.action} by {self.moderator.username}'
        self.assertEqual(str(moderation), expected_str)


class CommentReportModelTest(TestCase):
    """Test cases for CommentReport model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.reporter = User.objects.create_user(
            username='reporter',
            email='reporter@example.com',
            password='testpass123'
        )
        self.moderator = User.objects.create_user(
            username='moderator',
            email='moderator@example.com',
            password='testpass123'
        )
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.author,
            content='Content',
            category=self.category,
            status=self.status
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_comment_report_creation(self):
        """Test CommentReport creation."""
        report = CommentReport.objects.create(
            comment=self.comment,
            reporter=self.reporter,
            reason='spam',
            description='This comment is spam'
        )
        
        self.assertEqual(report.comment, self.comment)
        self.assertEqual(report.reporter, self.reporter)
        self.assertEqual(report.reason, 'spam')
        self.assertEqual(report.description, 'This comment is spam')
        self.assertEqual(report.status, 'pending')  # Default status
        self.assertIsNotNone(report.created_at)
        self.assertIsNone(report.resolved_at)
        self.assertIsNone(report.resolved_by)
    
    def test_comment_report_str_method(self):
        """Test CommentReport string representation."""
        report = CommentReport.objects.create(
            comment=self.comment,
            reporter=self.reporter,
            reason='spam'
        )
        expected_str = f'Report by {self.reporter.username} - spam'
        self.assertEqual(str(report), expected_str)
    
    def test_comment_report_resolution(self):
        """Test CommentReport resolution."""
        report = CommentReport.objects.create(
            comment=self.comment,
            reporter=self.reporter,
            reason='spam'
        )
        
        # Resolve the report
        report.status = 'resolved'
        report.resolved_at = timezone.now()
        report.resolved_by = self.moderator
        report.resolution_notes = 'Comment was removed'
        report.save()
        
        self.assertEqual(report.status, 'resolved')
        self.assertIsNotNone(report.resolved_at)
        self.assertEqual(report.resolved_by, self.moderator)
        self.assertEqual(report.resolution_notes, 'Comment was removed')


class ModelIntegrationTest(TestCase):
    """Integration tests for model relationships and signals."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.status = PostStatus.objects.create(
            name='Published',
            slug='published',
            is_published=True
        )
        self.tag = Tag.objects.create(name='Python', slug='python')
    
    def test_user_profile_signal(self):
        """Test that UserProfile is created automatically via signal."""
        # UserProfile should be created when User is created
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.user, self.user)
    
    def test_post_with_all_relationships(self):
        """Test Post creation with all relationships."""
        post = Post.objects.create(
            title='Complete Test Post',
            slug='complete-test-post',
            author=self.user,
            content='This is a complete test post with all relationships.',
            category=self.category,
            status=self.status
        )
        post.tags.add(self.tag)
        
        # Create engagement
        engagement = PostEngagement.objects.create(
            user=self.user,
            post=post,
            engagement_type='like'
        )
        
        # Create comment
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content='Great post!'
        )
        
        # Verify all relationships
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.status, self.status)
        self.assertIn(self.tag, post.tags.all())
        self.assertEqual(post.engagements.first(), engagement)
        self.assertEqual(post.comments.first(), comment)
    
    def test_cascade_deletions(self):
        """Test cascade deletion behavior."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Content',
            category=self.category,
            status=self.status
        )
        
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            content='Test comment'
        )
        
        engagement = PostEngagement.objects.create(
            user=self.user,
            post=post,
            engagement_type='like'
        )
        
        # Delete post should cascade to comments and engagements
        post_id = post.id
        post.delete()
        
        self.assertFalse(Comment.objects.filter(post_id=post_id).exists())
        self.assertFalse(PostEngagement.objects.filter(post_id=post_id).exists())
