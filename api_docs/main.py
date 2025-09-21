"""
FastAPI Documentation Application for Django Blog API.

This module creates a FastAPI application that mirrors the Django REST API
endpoints to provide comprehensive API documentation with Swagger UI.
The endpoints are documented but don't implement actual functionality -
they serve as documentation for the Django API.
"""

from fastapi import FastAPI, HTTPException, Query, Path, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from typing import List, Optional
import uvicorn

from .schemas import (
    # User schemas
    User, UserProfile,
    # Content schemas
    Category, Tag, PostStatus, PostList, PostDetail,
    # Engagement schemas
    PostEngagement,
    # Comment schemas
    Comment, CommentModeration, CommentReport,
    # Response schemas
    PaginatedResponse, ErrorResponse
)

from .config import (
    SWAGGER_UI_PARAMETERS,
    SWAGGER_UI_CSS,
    SWAGGER_UI_JS,
    OPENAPI_TAGS,
    OPENAPI_CUSTOM_FIELDS,
    SECURITY_SCHEMES,
    COMMON_RESPONSES,
    DEV_CONFIG
)

# =============================================================================
# FASTAPI APP CONFIGURATION
# =============================================================================

app = FastAPI(
    title="Django Blog API Documentation",
    description="""
    ## Interactive API Documentation for Django Blog Platform
    
    This is a comprehensive API documentation for the Django Blog Platform built with Django REST Framework.
    
    ### Features
    - **User Management**: User profiles and authentication
    - **Content Organization**: Categories and tags for organizing blog posts
    - **Blog Posts**: Full CRUD operations for blog posts with rich content
    - **Engagement**: Like/dislike functionality for posts
    - **Comments**: Nested commenting system with moderation
    - **Permissions**: Role-based access control
    
    ### Authentication
    Most endpoints require authentication using JWT tokens. Use the `/auth/login/` endpoint to obtain tokens.
    
    ### Rate Limiting
    API endpoints are rate-limited to prevent abuse. Check response headers for rate limit information.
    
    ### Pagination
    List endpoints support pagination with `page` and `page_size` parameters.
    
    ---
    
    **Note**: This is documentation-only. Actual API endpoints are served by the Django application at `/api/v1/`.
    """,
    version="1.0.0",
    contact={
        "name": "Django Blog API",
        "url": "http://127.0.0.1:8000/api/v1/",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=OPENAPI_TAGS,
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable ReDoc
    **OPENAPI_CUSTOM_FIELDS
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = SECURITY_SCHEMES
    
    # Add common responses
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "responses" not in openapi_schema["components"]:
        openapi_schema["components"]["responses"] = {}
    
    openapi_schema["components"]["responses"].update(COMMON_RESPONSES)
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_ui_parameters=SWAGGER_UI_PARAMETERS,
    )

# Custom CSS and JS injection
@app.get("/docs/custom.css", include_in_schema=False)
async def custom_css():
    return HTMLResponse(content=SWAGGER_UI_CSS, media_type="text/css")

@app.get("/docs/custom.js", include_in_schema=False)
async def custom_js():
    return HTMLResponse(content=SWAGGER_UI_JS, media_type="application/javascript")


# =============================================================================
# DEPENDENCY FUNCTIONS
# =============================================================================

def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page")
):
    """Get pagination parameters."""
    return {"page": page, "page_size": page_size}


def get_search_params(
    search: Optional[str] = Query(None, description="Search query"),
    ordering: Optional[str] = Query(None, description="Ordering field")
):
    """Get search and ordering parameters."""
    return {"search": search, "ordering": ordering}


# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


# =============================================================================
# USER ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/users/",
    response_model=PaginatedResponse,
    tags=["Users"],
    summary="List Users",
    description="Retrieve a paginated list of all users in the system."
)
async def list_users(
    pagination: dict = Depends(get_pagination_params),
    search: dict = Depends(get_search_params)
):
    """
    List all users with pagination and search capabilities.
    
    - **search**: Search by username, first name, or last name
    - **ordering**: Order by username, date_joined, etc.
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/users/{user_id}/",
    response_model=User,
    tags=["Users"],
    summary="Get User",
    description="Retrieve detailed information about a specific user."
)
async def get_user(
    user_id: int = Path(..., description="User ID")
):
    """Get user details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/user-profiles/",
    response_model=PaginatedResponse,
    tags=["User Profiles"],
    summary="List User Profiles",
    description="Retrieve a paginated list of all user profiles."
)
async def list_user_profiles(
    pagination: dict = Depends(get_pagination_params),
    search: dict = Depends(get_search_params)
):
    """List all user profiles with extended information."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/user-profiles/{profile_id}/",
    response_model=UserProfile,
    tags=["User Profiles"],
    summary="Get User Profile",
    description="Retrieve detailed user profile information."
)
async def get_user_profile(
    profile_id: int = Path(..., description="User Profile ID")
):
    """Get user profile details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# CATEGORY ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/categories/",
    response_model=PaginatedResponse,
    tags=["Categories"],
    summary="List Categories",
    description="Retrieve a paginated list of all blog categories."
)
async def list_categories(
    pagination: dict = Depends(get_pagination_params),
    search: dict = Depends(get_search_params),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    parent: Optional[int] = Query(None, description="Filter by parent category ID")
):
    """
    List all categories with filtering options.
    
    - **is_active**: Filter by active/inactive categories
    - **parent**: Filter by parent category (null for root categories)
    - **search**: Search by category name or description
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.post(
    "/api/v1/categories/",
    response_model=Category,
    tags=["Categories"],
    summary="Create Category",
    description="Create a new blog category.",
    status_code=201
)
async def create_category(category_data: dict):
    """Create a new category."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/categories/{category_id}/",
    response_model=Category,
    tags=["Categories"],
    summary="Get Category",
    description="Retrieve detailed information about a specific category."
)
async def get_category(
    category_id: int = Path(..., description="Category ID")
):
    """Get category details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/categories/{category_id}/posts/",
    response_model=PaginatedResponse,
    tags=["Categories"],
    summary="Get Category Posts",
    description="Retrieve all posts in a specific category."
)
async def get_category_posts(
    category_id: int = Path(..., description="Category ID"),
    pagination: dict = Depends(get_pagination_params)
):
    """Get all posts in a category."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# TAG ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/tags/",
    response_model=PaginatedResponse,
    tags=["Tags"],
    summary="List Tags",
    description="Retrieve a paginated list of all blog tags."
)
async def list_tags(
    pagination: dict = Depends(get_pagination_params),
    search: dict = Depends(get_search_params),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """
    List all tags with filtering options.
    
    - **is_active**: Filter by active/inactive tags
    - **search**: Search by tag name or description
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.post(
    "/api/v1/tags/",
    response_model=Tag,
    tags=["Tags"],
    summary="Create Tag",
    description="Create a new blog tag.",
    status_code=201
)
async def create_tag(tag_data: dict):
    """Create a new tag."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/tags/{tag_id}/",
    response_model=Tag,
    tags=["Tags"],
    summary="Get Tag",
    description="Retrieve detailed information about a specific tag."
)
async def get_tag(
    tag_id: int = Path(..., description="Tag ID")
):
    """Get tag details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/tags/{tag_id}/posts/",
    response_model=PaginatedResponse,
    tags=["Tags"],
    summary="Get Tag Posts",
    description="Retrieve all posts with a specific tag."
)
async def get_tag_posts(
    tag_id: int = Path(..., description="Tag ID"),
    pagination: dict = Depends(get_pagination_params)
):
    """Get all posts with a tag."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# POST STATUS ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/post-statuses/",
    response_model=PaginatedResponse,
    tags=["Post Statuses"],
    summary="List Post Statuses",
    description="Retrieve a paginated list of all post statuses."
)
async def list_post_statuses(
    pagination: dict = Depends(get_pagination_params),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_published: Optional[bool] = Query(None, description="Filter by published status")
):
    """
    List all post statuses.
    
    - **is_active**: Filter by active/inactive statuses
    - **is_published**: Filter by published/unpublished statuses
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/post-statuses/{status_id}/",
    response_model=PostStatus,
    tags=["Post Statuses"],
    summary="Get Post Status",
    description="Retrieve detailed information about a specific post status."
)
async def get_post_status(
    status_id: int = Path(..., description="Post Status ID")
):
    """Get post status details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# POST ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/posts/",
    response_model=PaginatedResponse,
    tags=["Posts"],
    summary="List Posts",
    description="Retrieve a paginated list of all blog posts."
)
async def list_posts(
    pagination: dict = Depends(get_pagination_params),
    search: dict = Depends(get_search_params),
    category: Optional[int] = Query(None, description="Filter by category ID"),
    tags: Optional[str] = Query(None, description="Filter by tag IDs (comma-separated)"),
    author: Optional[int] = Query(None, description="Filter by author ID"),
    status: Optional[int] = Query(None, description="Filter by status ID"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status")
):
    """
    List all posts with comprehensive filtering options.
    
    - **category**: Filter by category ID
    - **tags**: Filter by tag IDs (comma-separated, e.g., "1,2,3")
    - **author**: Filter by author user ID
    - **status**: Filter by post status ID
    - **is_featured**: Filter by featured status
    - **search**: Search in title, content, and excerpt
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.post(
    "/api/v1/posts/",
    response_model=PostDetail,
    tags=["Posts"],
    summary="Create Post",
    description="Create a new blog post.",
    status_code=201
)
async def create_post(post_data: dict):
    """Create a new blog post."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/posts/{post_id}/",
    response_model=PostDetail,
    tags=["Posts"],
    summary="Get Post",
    description="Retrieve detailed information about a specific post."
)
async def get_post(
    post_id: int = Path(..., description="Post ID")
):
    """Get post details by ID."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.put(
    "/api/v1/posts/{post_id}/",
    response_model=PostDetail,
    tags=["Posts"],
    summary="Update Post",
    description="Update an existing blog post."
)
async def update_post(
    post_id: int = Path(..., description="Post ID"),
    post_data: dict = None
):
    """Update a blog post."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.delete(
    "/api/v1/posts/{post_id}/",
    tags=["Posts"],
    summary="Delete Post",
    description="Delete a blog post.",
    status_code=204
)
async def delete_post(
    post_id: int = Path(..., description="Post ID")
):
    """Delete a blog post."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# ENGAGEMENT ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/engagements/",
    response_model=PaginatedResponse,
    tags=["Engagements"],
    summary="List Engagements",
    description="Retrieve a paginated list of all post engagements."
)
async def list_engagements(
    pagination: dict = Depends(get_pagination_params),
    post: Optional[int] = Query(None, description="Filter by post ID"),
    user: Optional[int] = Query(None, description="Filter by user ID"),
    engagement_type: Optional[str] = Query(None, description="Filter by engagement type")
):
    """
    List all post engagements.
    
    - **post**: Filter by post ID
    - **user**: Filter by user ID
    - **engagement_type**: Filter by type (like, bookmark, share, view)
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.post(
    "/api/v1/engagements/",
    response_model=PostEngagement,
    tags=["Engagements"],
    summary="Create Engagement",
    description="Create a new post engagement.",
    status_code=201
)
async def create_engagement(engagement_data: dict):
    """Create a new post engagement."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# COMMENT ENDPOINTS
# =============================================================================

@app.get(
    "/api/v1/comments/",
    response_model=PaginatedResponse,
    tags=["Comments"],
    summary="List Comments",
    description="Retrieve a paginated list of all comments."
)
async def list_comments(
    pagination: dict = Depends(get_pagination_params),
    post: Optional[int] = Query(None, description="Filter by post ID"),
    author: Optional[int] = Query(None, description="Filter by author ID"),
    is_approved: Optional[bool] = Query(None, description="Filter by approval status")
):
    """
    List all comments with filtering options.
    
    - **post**: Filter by post ID
    - **author**: Filter by comment author ID
    - **is_approved**: Filter by approval status
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/comment-moderations/",
    response_model=PaginatedResponse,
    tags=["Comment Moderation"],
    summary="List Comment Moderations",
    description="Retrieve a paginated list of all comment moderation actions."
)
async def list_comment_moderations(
    pagination: dict = Depends(get_pagination_params),
    action: Optional[str] = Query(None, description="Filter by moderation action")
):
    """List all comment moderation actions."""
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


@app.get(
    "/api/v1/comment-reports/",
    response_model=PaginatedResponse,
    tags=["Comment Reports"],
    summary="List Comment Reports",
    description="Retrieve a paginated list of all comment reports."
)
async def list_comment_reports(
    pagination: dict = Depends(get_pagination_params),
    status: Optional[str] = Query(None, description="Filter by report status"),
    reason: Optional[str] = Query(None, description="Filter by report reason")
):
    """
    List all comment reports.
    
    - **status**: Filter by report status (pending, under_review, resolved, dismissed)
    - **reason**: Filter by report reason (spam, harassment, etc.)
    """
    raise HTTPException(
        status_code=501,
        detail="This is a documentation endpoint. Use the Django API at the same path."
    )


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return ErrorResponse(detail="Not found", code="not_found")


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return ErrorResponse(detail="Internal server error", code="internal_error")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="info"
    )