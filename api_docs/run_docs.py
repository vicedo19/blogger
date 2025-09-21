#!/usr/bin/env python3
"""
FastAPI Documentation Server Runner

This script runs the FastAPI documentation server independently from Django.
It's useful for development and testing the API documentation.

Usage:
    python api_docs/run_docs.py

The documentation will be available at:
    - Swagger UI: http://localhost:8001/docs
    - OpenAPI JSON: http://localhost:8001/openapi.json
"""

import uvicorn
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from api_docs.main import app

if __name__ == "__main__":
    print("🚀 Starting FastAPI Documentation Server...")
    print("📚 Swagger UI: http://localhost:8001/docs")
    print("📋 OpenAPI JSON: http://localhost:8001/openapi.json")
    print("🔄 Auto-reload enabled for development")
    print("⏹️  Press Ctrl+C to stop the server")
    
    uvicorn.run(
        "api_docs.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        reload_dirs=[project_root],
        log_level="info"
    )