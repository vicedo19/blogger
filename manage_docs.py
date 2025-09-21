#!/usr/bin/env python3
"""
Django + FastAPI Documentation Integration

This script provides integration between Django and FastAPI documentation.
It can run both servers simultaneously or just the documentation server.

Usage:
    python manage_docs.py --docs-only    # Run only FastAPI docs server
    python manage_docs.py --both         # Run both Django and FastAPI servers
    python manage_docs.py --help         # Show help
"""

import os
import sys
import subprocess
import threading
import time
import argparse
from pathlib import Path

# Add Django project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_django_server():
    """Run Django development server"""
    print("🔧 Starting Django development server...")
    try:
        subprocess.run([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ], cwd=project_root, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Django server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Django server failed: {e}")

def run_fastapi_docs():
    """Run FastAPI documentation server"""
    print("📚 Starting FastAPI documentation server...")
    try:
        subprocess.run([
            sys.executable, "api_docs/run_docs.py"
        ], cwd=project_root, check=True)
    except KeyboardInterrupt:
        print("\n🛑 FastAPI docs server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI docs server failed: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Django + FastAPI Documentation Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_docs.py --docs-only    Run only FastAPI documentation server
  python manage_docs.py --both         Run both Django and FastAPI servers
  
URLs:
  Django API:     http://127.0.0.1:8000/api/v1/
  FastAPI Docs:   http://127.0.0.1:8001/docs
  OpenAPI JSON:   http://127.0.0.1:8001/openapi.json
        """
    )
    
    parser.add_argument(
        "--docs-only",
        action="store_true",
        help="Run only the FastAPI documentation server"
    )
    
    parser.add_argument(
        "--both",
        action="store_true",
        help="Run both Django and FastAPI servers simultaneously"
    )
    
    args = parser.parse_args()
    
    if not args.docs_only and not args.both:
        parser.print_help()
        return
    
    print("=" * 60)
    print("🚀 Django + FastAPI Documentation Integration")
    print("=" * 60)
    
    if args.docs_only:
        print("📚 Running FastAPI documentation server only...")
        print("🔗 Documentation: http://127.0.0.1:8001/docs")
        run_fastapi_docs()
    
    elif args.both:
        print("🔧 Running both Django and FastAPI servers...")
        print("🔗 Django API: http://127.0.0.1:8000/api/v1/")
        print("🔗 FastAPI Docs: http://127.0.0.1:8001/docs")
        
        # Start Django server in a separate thread
        django_thread = threading.Thread(target=run_django_server, daemon=True)
        django_thread.start()
        
        # Give Django server time to start
        time.sleep(2)
        
        # Start FastAPI docs server (this will block)
        try:
            run_fastapi_docs()
        except KeyboardInterrupt:
            print("\n🛑 Stopping all servers...")

if __name__ == "__main__":
    main()