"""
Master management command to populate default values for all choice models.

This command runs all individual populate commands for each app:
- accounts: Hardcoded choice fields (UserActivity, UserPreferences)
- blog_app: PostStatus (dynamic model)
- comments: Hardcoded choice fields (CommentModeration, CommentReport)
- media: Hardcoded choice fields (MediaFile, DocumentFile)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Populate default values for all choice models across all apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of all default values (will delete existing)',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS('Starting population of all choice models...')
        )

        # List of commands to run
        commands = [
            ('populate_account_choices', 'accounts app'),
            ('populate_blog_choices', 'blog_app'),
            ('populate_comments_choices', 'comments app'),
            ('populate_media_choices', 'media app'),
        ]

        for command_name, app_description in commands:
            try:
                self.stdout.write(f"\nPopulating {app_description}...")
                
                # Prepare arguments
                command_args = []
                if force:
                    command_args.append('--force')
                
                # Call the individual command
                call_command(command_name, *command_args)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Successfully populated {app_description}")
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed to populate {app_description}: {e}")
                )

        self.stdout.write(
            self.style.SUCCESS('\n🎉 All choice models population completed!')
        )
        
        # Provide usage instructions
        self.stdout.write(
            self.style.WARNING('\nNext steps:')
        )
        self.stdout.write('1. Check the Django admin to verify all choice models are populated')
        self.stdout.write('2. Test creating new records that use these choice fields')
        self.stdout.write('3. Update any existing records to use the new choice models if needed')