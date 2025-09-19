"""
Management command to populate default values for accounts app choice models.

Note: The accounts app currently uses hardcoded choices in UserActivity and UserPreferences.
This command serves as a placeholder for future dynamic choice model implementation.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import UserActivity, UserPreferences


class Command(BaseCommand):
    help = 'Populate default values for accounts app choice models (placeholder for future implementation)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of all default values (will delete existing)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'The accounts app currently uses hardcoded choices in UserActivity and UserPreferences models.'
            )
        )
        self.stdout.write(
            'To implement dynamic choice models, the following models need to be created:'
        )
        self.stdout.write('- ActivityType (for UserActivity.activity_type)')
        self.stdout.write('- ProfileVisibility (for UserPreferences.profile_visibility)')
        self.stdout.write('- ThemePreference (for UserPreferences.theme_preference)')
        
        self.stdout.write(
            self.style.SUCCESS('Accounts app choice models review completed')
        )

    def _populate_activity_types(self):
        """Populate default activity types."""
        activity_types = [
            {
                'name': 'Login',
                'slug': 'login',
                'description': 'User logged into the system',
                'is_active': True,
                'sort_order': 1,
            },
            {
                'name': 'Logout',
                'slug': 'logout',
                'description': 'User logged out of the system',
                'is_active': True,
                'sort_order': 2,
            },
            {
                'name': 'Profile Update',
                'slug': 'profile-update',
                'description': 'User updated their profile information',
                'is_active': True,
                'sort_order': 3,
            },
            {
                'name': 'Password Change',
                'slug': 'password-change',
                'description': 'User changed their password',
                'is_active': True,
                'sort_order': 4,
            },
            {
                'name': 'Email Verification',
                'slug': 'email-verification',
                'description': 'User verified their email address',
                'is_active': True,
                'sort_order': 5,
            },
            {
                'name': 'Account Creation',
                'slug': 'account-creation',
                'description': 'New user account was created',
                'is_active': True,
                'sort_order': 6,
            },
            {
                'name': 'Account Deletion',
                'slug': 'account-deletion',
                'description': 'User account was deleted',
                'is_active': True,
                'sort_order': 7,
            },
            {
                'name': 'Failed Login',
                'slug': 'failed-login',
                'description': 'Failed login attempt',
                'is_active': True,
                'sort_order': 8,
            },
        ]

        created_count = 0
        for activity_data in activity_types:
            activity_type, created = ActivityType.objects.get_or_create(
                slug=activity_data['slug'],
                defaults=activity_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created ActivityType: {activity_type.name}")

        self.stdout.write(f"ActivityTypes: {created_count} created")

    def _populate_moderation_actions(self):
        """Populate default moderation actions."""
        moderation_actions = [
            {
                'name': 'Warning',
                'slug': 'warning',
                'description': 'Issue a warning to the user',
                'is_active': True,
                'is_destructive': False,
                'sort_order': 1,
            },
            {
                'name': 'Temporary Suspension',
                'slug': 'temp-suspension',
                'description': 'Temporarily suspend user account',
                'is_active': True,
                'is_destructive': True,
                'sort_order': 2,
            },
            {
                'name': 'Permanent Ban',
                'slug': 'permanent-ban',
                'description': 'Permanently ban user account',
                'is_active': True,
                'is_destructive': True,
                'sort_order': 3,
            },
            {
                'name': 'Content Removal',
                'slug': 'content-removal',
                'description': 'Remove user-generated content',
                'is_active': True,
                'is_destructive': True,
                'sort_order': 4,
            },
            {
                'name': 'Account Verification',
                'slug': 'account-verification',
                'description': 'Verify user account authenticity',
                'is_active': True,
                'is_destructive': False,
                'sort_order': 5,
            },
            {
                'name': 'Privilege Revocation',
                'slug': 'privilege-revocation',
                'description': 'Revoke specific user privileges',
                'is_active': True,
                'is_destructive': True,
                'sort_order': 6,
            },
            {
                'name': 'Account Restoration',
                'slug': 'account-restoration',
                'description': 'Restore previously suspended account',
                'is_active': True,
                'is_destructive': False,
                'sort_order': 7,
            },
            {
                'name': 'Content Approval',
                'slug': 'content-approval',
                'description': 'Approve user-submitted content',
                'is_active': True,
                'is_destructive': False,
                'sort_order': 8,
            },
        ]

        created_count = 0
        for action_data in moderation_actions:
            moderation_action, created = ModerationAction.objects.get_or_create(
                slug=action_data['slug'],
                defaults=action_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created ModerationAction: {moderation_action.name}")

        self.stdout.write(f"ModerationActions: {created_count} created")