"""
Configuration for FastAPI Documentation Application.

This module contains configuration settings for the FastAPI documentation app,
including custom Swagger UI styling and OpenAPI customizations.
"""

from typing import Dict, Any

# =============================================================================
# SWAGGER UI CONFIGURATION
# =============================================================================

SWAGGER_UI_PARAMETERS = {
    "deepLinking": True,
    "displayRequestDuration": True,
    "docExpansion": "none",
    "operationsSorter": "method",
    "filter": True,
    "showExtensions": True,
    "showCommonExtensions": True,
    "tryItOutEnabled": True,
    "requestSnippetsEnabled": True,
    "persistAuthorization": True,
    "displayOperationId": False,
    "defaultModelsExpandDepth": 2,
    "defaultModelExpandDepth": 2,
    "defaultModelRendering": "model",
    "showMutatedRequest": True,
    "supportedSubmitMethods": ["get", "post", "put", "delete", "patch"],
}

# Custom CSS for Swagger UI
SWAGGER_UI_CSS = """
<style>
    /* Custom color scheme */
    .swagger-ui .topbar { 
        background-color: #1f2937; 
        border-bottom: 3px solid #3b82f6;
    }
    
    .swagger-ui .topbar .download-url-wrapper { 
        display: none; 
    }
    
    /* Header styling */
    .swagger-ui .info .title {
        color: #1f2937;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .swagger-ui .info .description {
        color: #4b5563;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Operation styling */
    .swagger-ui .opblock.opblock-get {
        border-color: #10b981;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .swagger-ui .opblock.opblock-post {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .swagger-ui .opblock.opblock-put {
        border-color: #f59e0b;
        background: rgba(245, 158, 11, 0.1);
    }
    
    .swagger-ui .opblock.opblock-delete {
        border-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }
    
    /* Button styling */
    .swagger-ui .btn.authorize {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    
    .swagger-ui .btn.authorize:hover {
        background-color: #2563eb;
        border-color: #2563eb;
    }
    
    /* Schema styling */
    .swagger-ui .model-box {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
    }
    
    .swagger-ui .model .model-title {
        color: #1f2937;
        font-weight: 600;
    }
    
    /* Response styling */
    .swagger-ui .responses-inner h4 {
        color: #1f2937;
        font-weight: 600;
    }
    
    /* Parameter styling */
    .swagger-ui .parameters-col_description p {
        color: #6b7280;
        margin: 0;
    }
    
    /* Tag styling */
    .swagger-ui .opblock-tag {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    /* Try it out button */
    .swagger-ui .btn.try-out__btn {
        background-color: #059669;
        border-color: #059669;
        color: white;
    }
    
    .swagger-ui .btn.try-out__btn:hover {
        background-color: #047857;
        border-color: #047857;
    }
    
    /* Execute button */
    .swagger-ui .btn.execute {
        background-color: #3b82f6;
        border-color: #3b82f6;
    }
    
    .swagger-ui .btn.execute:hover {
        background-color: #2563eb;
        border-color: #2563eb;
    }
    
    /* Custom scrollbar */
    .swagger-ui ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    .swagger-ui ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    .swagger-ui ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    .swagger-ui ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .swagger-ui .info .title {
            font-size: 2rem;
        }
        
        .swagger-ui .opblock-summary {
            flex-wrap: wrap;
        }
    }
</style>
"""

# Custom JavaScript for enhanced functionality
SWAGGER_UI_JS = """
<script>
    // Custom JavaScript for enhanced Swagger UI functionality
    window.onload = function() {
        // Add custom behavior after Swagger UI loads
        console.log('Django Blog API Documentation loaded');
        
        // Auto-expand first operation in each tag
        setTimeout(() => {
            const firstOperations = document.querySelectorAll('.opblock-tag-section .opblock:first-child');
            firstOperations.forEach(op => {
                const summary = op.querySelector('.opblock-summary');
                if (summary && !op.classList.contains('is-open')) {
                    summary.click();
                }
            });
        }, 1000);
    };
</script>
"""

# =============================================================================
# OPENAPI CONFIGURATION
# =============================================================================

OPENAPI_TAGS = [
    {
        "name": "Users",
        "description": "User management operations. Handle user accounts and basic user information.",
    },
    {
        "name": "User Profiles",
        "description": "Extended user profile operations. Manage user profiles with additional information like bio, avatar, and preferences.",
    },
    {
        "name": "Categories",
        "description": "Blog category management. Organize posts into hierarchical categories with custom styling and metadata.",
    },
    {
        "name": "Tags",
        "description": "Tag management operations. Create and manage tags for post classification and filtering.",
    },
    {
        "name": "Post Statuses",
        "description": "Post status management. Define and manage different post publication states.",
    },
    {
        "name": "Posts",
        "description": "Blog post operations. Full CRUD operations for blog posts with rich content, metadata, and relationships.",
    },
    {
        "name": "Engagements",
        "description": "User engagement tracking. Track likes, bookmarks, shares, and views on blog posts.",
    },
    {
        "name": "Comments",
        "description": "Comment system operations. Manage threaded comments on blog posts with approval workflow.",
    },
    {
        "name": "Comment Moderation",
        "description": "Comment moderation operations. Administrative tools for moderating user comments.",
    },
    {
        "name": "Comment Reports",
        "description": "Comment reporting system. Handle user reports of inappropriate comments with resolution workflow.",
    },
]

# Custom OpenAPI schema modifications
OPENAPI_CUSTOM_FIELDS = {
    "x-logo": {
        "url": "/static/logo.png",
        "altText": "Django Blog API"
    },
    "x-api-id": "django-blog-api",
    "x-audience": "developers",
}

# Security schemes for authentication
SECURITY_SCHEMES = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token authentication. Include the token in the Authorization header."
    },
    "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
        "description": "API key authentication for service-to-service communication."
    }
}

# Example responses for common HTTP status codes
COMMON_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "detail": "Invalid input data",
                    "code": "bad_request"
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "detail": "Authentication credentials were not provided",
                    "code": "unauthorized"
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "detail": "You do not have permission to perform this action",
                    "code": "forbidden"
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "detail": "Not found",
                    "code": "not_found"
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ErrorResponse"},
                "example": {
                    "detail": "Internal server error",
                    "code": "internal_error"
                }
            }
        }
    }
}

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

DEV_CONFIG = {
    "host": "127.0.0.1",
    "port": 8001,
    "reload": True,
    "log_level": "info",
    "access_log": True,
}

# =============================================================================
# PRODUCTION CONFIGURATION
# =============================================================================

PROD_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,
    "reload": False,
    "log_level": "warning",
    "access_log": False,
    "workers": 4,
}