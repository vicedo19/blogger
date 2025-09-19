"""Management command to populate default values for media app choice models.

Note: The media app currently uses hardcoded choices in MediaFile and DocumentFile.
This command serves as a placeholder for future dynamic choice model implementation.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from media.models import MediaFile, DocumentFile


class Command(BaseCommand):
    help = 'Populate default values for media app choice models (placeholder for future implementation)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreation of all default values (will delete existing)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'The media app currently uses hardcoded choices in MediaFile and DocumentFile models.'
            )
        )
        self.stdout.write(
            'To implement dynamic choice models, the following models need to be created:'
        )
        self.stdout.write('- FileType (for MediaFile.file_type)')
        self.stdout.write('- DocumentCategory (for DocumentFile.category)')
        
        self.stdout.write(
            self.style.SUCCESS('Media app choice models review completed')
        )

    def _populate_file_types(self):
        """Populate default file types."""
        file_types = [
            {
                'name': 'Image',
                'slug': 'image',
                'is_active': True,
                'sort_order': 1,
            },
            {
                'name': 'Document',
                'slug': 'document',
                'is_active': True,
                'sort_order': 2,
            },
            {
                'name': 'Video',
                'slug': 'video',
                'is_active': True,
                'sort_order': 3,
            },
            {
                'name': 'Audio',
                'slug': 'audio',
                'is_active': True,
                'sort_order': 4,
            },
            {
                'name': 'Archive',
                'slug': 'archive',
                'is_active': True,
                'sort_order': 5,
            },
            {
                'name': 'Other',
                'slug': 'other',
                'is_active': True,
                'sort_order': 6,
            },
        ]

        created_count = 0
        for file_type_data in file_types:
            file_type, created = FileType.objects.get_or_create(
                slug=file_type_data['slug'],
                defaults=file_type_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created FileType: {file_type.name}")

        self.stdout.write(f"FileTypes: {created_count} created")

    def _populate_document_categories(self):
        """Populate default document categories."""
        document_categories = [
            {
                'name': 'Report',
                'slug': 'report',
                'is_active': True,
                'sort_order': 1,
            },
            {
                'name': 'Presentation',
                'slug': 'presentation',
                'is_active': True,
                'sort_order': 2,
            },
            {
                'name': 'Spreadsheet',
                'slug': 'spreadsheet',
                'is_active': True,
                'sort_order': 3,
            },
            {
                'name': 'Text Document',
                'slug': 'text-document',
                'is_active': True,
                'sort_order': 4,
            },
            {
                'name': 'PDF',
                'slug': 'pdf',
                'is_active': True,
                'sort_order': 5,
            },
            {
                'name': 'Contract',
                'slug': 'contract',
                'is_active': True,
                'sort_order': 6,
            },
            {
                'name': 'Invoice',
                'slug': 'invoice',
                'is_active': True,
                'sort_order': 7,
            },
            {
                'name': 'Manual',
                'slug': 'manual',
                'is_active': True,
                'sort_order': 8,
            },
            {
                'name': 'Other',
                'slug': 'other',
                'is_active': True,
                'sort_order': 9,
            },
        ]

        created_count = 0
        for category_data in document_categories:
            document_category, created = DocumentCategory.objects.get_or_create(
                slug=category_data['slug'],
                defaults=category_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created DocumentCategory: {document_category.name}")

        self.stdout.write(f"DocumentCategories: {created_count} created")