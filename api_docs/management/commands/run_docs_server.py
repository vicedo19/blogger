"""
Django management command to run the FastAPI documentation server.

This command starts the FastAPI application that serves the API documentation
using Swagger UI and OpenAPI specification.
"""

import os
import sys
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Run the FastAPI documentation server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            type=str,
            default='127.0.0.1',
            help='Host to bind the server to (default: 127.0.0.1)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=8001,
            help='Port to bind the server to (default: 8001)'
        )
        parser.add_argument(
            '--reload',
            action='store_true',
            help='Enable auto-reload for development'
        )
        parser.add_argument(
            '--log-level',
            type=str,
            default='info',
            choices=['critical', 'error', 'warning', 'info', 'debug', 'trace'],
            help='Log level (default: info)'
        )

    def handle(self, *args, **options):
        try:
            import uvicorn
        except ImportError:
            self.stdout.write(
                self.style.ERROR(
                    'uvicorn is not installed. Please install it with: pip install uvicorn'
                )
            )
            return

        host = options['host']
        port = options['port']
        reload = options['reload']
        log_level = options['log_level']

        self.stdout.write(
            self.style.SUCCESS(
                f'Starting FastAPI documentation server at http://{host}:{port}'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Swagger UI will be available at http://{host}:{port}/docs'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'OpenAPI spec will be available at http://{host}:{port}/openapi.json'
            )
        )

        # Add the project root to Python path
        project_root = Path(settings.BASE_DIR)
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        try:
            uvicorn.run(
                "api_docs.app:app",
                host=host,
                port=port,
                reload=reload,
                log_level=log_level,
                access_log=True
            )
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.SUCCESS('\nDocumentation server stopped.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error starting server: {e}')
            )