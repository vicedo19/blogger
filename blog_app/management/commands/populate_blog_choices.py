"""
Management command to populate default values for blog_app choice models.

This command creates default entries for:
- PostStatus: Common blog post statuses
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from blog_app.models import PostStatus


class Command(BaseCommand):
    help = 'Populate default values for blog_app choice models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of all default values (will delete existing)',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        if force:
            self.stdout.write(
                self.style.WARNING('Force mode enabled - deleting existing data')
            )
            PostStatus.objects.all().delete()

        with transaction.atomic():
            self._populate_post_statuses()

        self.stdout.write(
            self.style.SUCCESS('Successfully populated blog_app choice models')
        )

    def _populate_post_statuses(self):
        """Populate default post statuses."""
        post_statuses = [
            {
                'name': 'Draft',
                'slug': 'draft',
                'description': 'Post is in draft mode and not published',
                'is_active': True,
                'is_published': False,
                'sort_order': 1,
            },
            {
                'name': 'Published',
                'slug': 'published',
                'description': 'Post is published and visible to public',
                'is_active': True,
                'is_published': True,
                'sort_order': 2,
            },
            {
                'name': 'Scheduled',
                'slug': 'scheduled',
                'description': 'Post is scheduled for future publication',
                'is_active': True,
                'is_published': False,
                'sort_order': 3,
            },
            {
                'name': 'Under Review',
                'slug': 'under-review',
                'description': 'Post is under editorial review',
                'is_active': True,
                'is_published': False,
                'sort_order': 4,
            },
            {
                'name': 'Archived',
                'slug': 'archived',
                'description': 'Post is archived and no longer active',
                'is_active': False,
                'is_published': False,
                'sort_order': 5,
            },
            {
                'name': 'Rejected',
                'slug': 'rejected',
                'description': 'Post was rejected during review process',
                'is_active': False,
                'is_published': False,
                'sort_order': 6,
            },
            {
                'name': 'Private',
                'slug': 'private',
                'description': 'Post is private and only visible to author',
                'is_active': True,
                'is_published': False,
                'sort_order': 7,
            },
            {
                'name': 'Pending',
                'slug': 'pending',
                'description': 'Post is pending approval for publication',
                'is_active': True,
                'is_published': False,
                'sort_order': 8,
            },
        ]

        created_count = 0
        for status_data in post_statuses:
            post_status, created = PostStatus.objects.get_or_create(
                slug=status_data['slug'],
                defaults=status_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created PostStatus: {post_status.name}")

        self.stdout.write(f"PostStatuses: {created_count} created")