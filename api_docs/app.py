"""
FastAPI application for API documentation.

This module creates a FastAPI application specifically for generating
comprehensive API documentation using Swagger UI and OpenAPI specification.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path for Django imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogger.settings')

import django
django.setup()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import router

# Create FastAPI application
app = FastAPI(
    title="Blog API Documentation",
    description="""
    ## Comprehensive Blog API Documentation
    
    This documentation provides detailed information about all available endpoints
    in the Blog application's REST API. The API is built using Django REST Framework
    and provides comprehensive functionality for managing blog posts, comments, 
    categories, tags, and user interactions.
    
    ### Features
    
    * **Posts Management**: Create, read, update, and delete blog posts
    * **Comments System**: Nested comments with moderation capabilities
    * **Categories & Tags**: Organize content with hierarchical categories and flexible tagging
    * **Advanced Filtering**: Comprehensive filtering options for all resources
    * **Search Functionality**: Full-text search across posts and comments
    * **Pagination**: Efficient pagination for large datasets
    * **Authentication**: JWT-based authentication system
    * **Permissions**: Role-based access control
    
    ### Authentication
    
    Most endpoints require authentication using JWT tokens. Include the token
    in the Authorization header:
    
    ```
    Authorization: Bearer <your-jwt-token>
    ```
    
    ### Filtering and Search
    
    The API supports extensive filtering and search capabilities:
    
    * **Text Search**: Use the `search` parameter for full-text search
    * **Field Filters**: Filter by specific field values
    * **Date Ranges**: Filter by creation/update dates
    * **Boolean Filters**: Filter by true/false values
    * **Numeric Ranges**: Filter by numeric ranges (word count, etc.)
    
    ### Pagination
    
    List endpoints return paginated results with the following structure:
    
    ```json
    {
        "count": 100,
        "next": "http://example.com/api/posts/?page=3",
        "previous": "http://example.com/api/posts/?page=1",
        "results": [...]
    }
    ```
    
    ### Error Handling
    
    The API uses standard HTTP status codes and returns detailed error messages:
    
    * **400 Bad Request**: Invalid request data
    * **401 Unauthorized**: Authentication required
    * **403 Forbidden**: Insufficient permissions
    * **404 Not Found**: Resource not found
    * **422 Unprocessable Entity**: Validation errors
    
    ### Rate Limiting
    
    API endpoints are rate-limited to ensure fair usage and system stability.
    """,
    version="1.0.0",
    contact={
        "name": "Blog API Support",
        "email": "support@blogapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "Posts",
            "description": "Operations with blog posts. Create, read, update, delete posts with advanced filtering and search capabilities.",
        },
        {
            "name": "Comments",
            "description": "Operations with comments. Manage nested comments with moderation features.",
        },
        {
            "name": "Categories",
            "description": "Operations with categories. Organize posts into hierarchical categories.",
        },
        {
            "name": "Tags",
            "description": "Operations with tags. Flexible tagging system for content organization.",
        },
        {
            "name": "Post Status",
            "description": "Operations with post statuses. Manage publication workflow states.",
        },
    ],
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://your-production-domain.com",
            "description": "Production server"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides basic API information.
    
    Returns welcome message and links to documentation.
    """
    return {
        "message": "Welcome to the Blog API Documentation",
        "documentation": "/docs",
        "openapi_spec": "/openapi.json",
        "version": "1.0.0",
        "endpoints": {
            "posts": "/api/v1/posts/",
            "comments": "/api/v1/comments/",
            "categories": "/api/v1/categories/",
            "tags": "/api/v1/tags/",
            "post_statuses": "/api/v1/post-statuses/"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns the current status of the API documentation service.
    """
    return {
        "status": "healthy",
        "service": "Blog API Documentation",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_docs.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )