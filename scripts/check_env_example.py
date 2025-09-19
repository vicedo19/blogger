#!/usr/bin/env python3
"""
Script to check if .env.example file exists and contains all required environment variables.
This is used as a pre-commit hook to ensure environment configuration is properly documented.
"""

import os
import sys
from pathlib import Path
from typing import Set, List


def get_env_vars_from_code() -> Set[str]:
    """Extract environment variables used in the codebase."""
    env_vars = set()
    
    # Common Django environment variables
    django_vars = {
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASE_ENGINE',
        'DATABASE_NAME',
        'DATABASE_USER',
        'DATABASE_PASSWORD',
        'DATABASE_HOST',
        'DATABASE_PORT',
        'REDIS_URL',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_USE_TLS',
        'STATIC_URL',
        'MEDIA_URL',
        'SENTRY_DSN',
    }
    
    env_vars.update(django_vars)
    
    # Scan Python files for config() calls
    project_root = Path('.')
    for py_file in project_root.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for config('VAR_NAME') patterns
            import re
            pattern = r"config\(['\"]([A-Z_]+)['\"]"
            matches = re.findall(pattern, content)
            env_vars.update(matches)
            
        except (UnicodeDecodeError, PermissionError):
            continue
    
    return env_vars


def get_env_vars_from_example() -> Set[str]:
    """Extract environment variables from .env.example file."""
    env_example_path = Path('.env.example')
    
    if not env_example_path.exists():
        return set()
    
    env_vars = set()
    
    try:
        with open(env_example_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    var_name = line.split('=')[0].strip()
                    env_vars.add(var_name)
    except (UnicodeDecodeError, PermissionError):
        pass
    
    return env_vars


def create_env_example_template(missing_vars: Set[str]) -> str:
    """Create a template for .env.example with missing variables."""
    template_lines = [
        "# Django Configuration",
        "SECRET_KEY=your-secret-key-here",
        "DEBUG=False",
        "ALLOWED_HOSTS=localhost,127.0.0.1",
        "",
        "# Database Configuration",
        "DATABASE_ENGINE=django.db.backends.postgresql",
        "DATABASE_NAME=blogger",
        "DATABASE_USER=blogger_user",
        "DATABASE_PASSWORD=blogger_password",
        "DATABASE_HOST=localhost",
        "DATABASE_PORT=5432",
        "",
        "# Redis Configuration",
        "REDIS_URL=redis://localhost:6379/0",
        "",
        "# Email Configuration",
        "EMAIL_HOST=smtp.gmail.com",
        "EMAIL_PORT=587",
        "EMAIL_HOST_USER=your-email@gmail.com",
        "EMAIL_HOST_PASSWORD=your-app-password",
        "EMAIL_USE_TLS=True",
        "",
        "# Static and Media Files",
        "STATIC_URL=/static/",
        "MEDIA_URL=/media/",
        "",
        "# Monitoring (Optional)",
        "SENTRY_DSN=your-sentry-dsn-here",
    ]
    
    # Add any additional missing variables
    additional_vars = missing_vars - {
        'SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'DATABASE_ENGINE',
        'DATABASE_NAME', 'DATABASE_USER', 'DATABASE_PASSWORD',
        'DATABASE_HOST', 'DATABASE_PORT', 'REDIS_URL', 'EMAIL_HOST',
        'EMAIL_PORT', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD',
        'EMAIL_USE_TLS', 'STATIC_URL', 'MEDIA_URL', 'SENTRY_DSN'
    }
    
    if additional_vars:
        template_lines.extend([
            "",
            "# Additional Configuration",
        ])
        for var in sorted(additional_vars):
            template_lines.append(f"{var}=")
    
    return '\n'.join(template_lines)


def main() -> int:
    """Main function to check environment configuration."""
    print("Checking .env.example file...")
    
    # Get environment variables from code and example file
    code_vars = get_env_vars_from_code()
    example_vars = get_env_vars_from_example()
    
    # Check if .env.example exists
    env_example_path = Path('.env.example')
    if not env_example_path.exists():
        print("❌ .env.example file does not exist!")
        print("Creating .env.example template...")
        
        template = create_env_example_template(code_vars)
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print("✅ Created .env.example template")
        print("Please review and update the values as needed.")
        return 1
    
    # Check for missing variables
    missing_vars = code_vars - example_vars
    
    if missing_vars:
        print(f"❌ Missing environment variables in .env.example:")
        for var in sorted(missing_vars):
            print(f"  - {var}")
        
        print("\nPlease add these variables to .env.example")
        return 1
    
    # Check for unused variables (optional warning)
    unused_vars = example_vars - code_vars
    if unused_vars:
        print(f"⚠️  Potentially unused environment variables in .env.example:")
        for var in sorted(unused_vars):
            print(f"  - {var}")
        print("(This is just a warning, not an error)")
    
    print("✅ .env.example file is up to date!")
    return 0


if __name__ == '__main__':
    sys.exit(main())