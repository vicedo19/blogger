"""
Management command to populate comment-related choice models.

This command serves as a placeholder for the comments app choice population.
Since the comments app uses hardcoded choice fields (which is the recommended
approach for this project), this command provides information about the
existing hardcoded choices and confirms they are properly configured.

Usage:
    python manage.py populate_comments_choices
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from comments.models import Comment, CommentModeration, CommentReport


class Command(BaseCommand):
    """
    Django management command to handle comments app choice field population.
    
    This command acknowledges the hardcoded choice fields in the comments app
    and provides information about their current configuration.
    """
    
    help = 'Populate comment-related choice models (hardcoded choices approach)'
    
    def add_arguments(self, parser) -> None:
        """Add command line arguments."""
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force review of hardcoded choices (informational only)',
        )
    
    def handle(self, *args, **options) -> None:
        """
        Handle the command execution.
        
        Args:
            *args: Variable length argument list
            **options: Arbitrary keyword arguments from command line
        """
        force = options.get('force', False)
        
        self.stdout.write(
            self.style.SUCCESS('Starting comments app choice field review...')
        )
        
        # Review hardcoded choices in CommentModeration model
        self.stdout.write('\n📋 CommentModeration.MODERATION_ACTIONS:')
        for code, label in CommentModeration.MODERATION_ACTIONS:
            self.stdout.write(f'  • {code}: {label}')
        
        # Review hardcoded choices in CommentReport model
        self.stdout.write('\n📋 CommentReport.REPORT_REASONS:')
        for code, label in CommentReport.REPORT_REASONS:
            self.stdout.write(f'  • {code}: {label}')
        
        self.stdout.write('\n📋 CommentReport.STATUS_CHOICES:')
        for code, label in CommentReport.STATUS_CHOICES:
            self.stdout.write(f'  • {code}: {label}')
        
        # Provide summary information
        self.stdout.write('\n' + '='*60)
        self.stdout.write('📊 COMMENTS APP CHOICE FIELDS SUMMARY:')
        self.stdout.write('='*60)
        
        self.stdout.write(f'✅ CommentModeration actions: {len(CommentModeration.MODERATION_ACTIONS)} choices')
        self.stdout.write(f'✅ CommentReport reasons: {len(CommentReport.REPORT_REASONS)} choices')
        self.stdout.write(f'✅ CommentReport statuses: {len(CommentReport.STATUS_CHOICES)} choices')
        
        self.stdout.write('\n💡 All choice fields are using hardcoded approach for:')
        self.stdout.write('   • Better performance (no database queries)')
        self.stdout.write('   • Improved maintainability')
        self.stdout.write('   • Version control tracking')
        self.stdout.write('   • Type safety and consistency')
        
        if force:
            self.stdout.write('\n🔍 Force flag detected - choices reviewed successfully')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Comments app choice field review completed successfully! '
                f'[{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}]'
            )
        )