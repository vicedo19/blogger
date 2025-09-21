"""
Pydantic schemas for FastAPI API documentation.

This module contains Pydantic models that mirror the Django models
to provide comprehensive API documentation with proper type hints,
validation, and examples for Swagger UI.
"""

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from enum import Enum


# =============================================================================
# ENUMS AND CHOICES
# =============================================================================

class EngagementType(str, Enum):
    """Engagement type choices."""
    like = "like"
    bookmark = "bookmark"
    share = "share"
    view = "view"


class ModerationAction(str, Enum):
    """Moderation action choices."""
    approved = "approved"
    rejected = "rejected"
    flagged = "flagged"
    spam = "spam"
    edited = "edited"


class ReportReason(str, Enum):
    """Report reason choices."""
    spam = "spam"
    harassment = "harassment"
    inappropriate = "inappropriate"
    off_topic = "off_topic"
    misinformation = "misinformation"
    copyright = "copyright"
    other = "other"


class ReportStatus(str, Enum):
    """Report status choices."""
    pending = "pending"
    under_review = "under_review"
    resolved = "resolved"
    dismissed = "dismissed"


# =============================================================================
# BASE SCHEMAS
# =============================================================================

class BaseSchema(BaseModel):
    """Base schema with common fields."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# =============================================================================
# USER SCHEMAS
# =============================================================================

class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=1, max_length=150, description="Username")
    email: Optional[EmailStr] = Field(None, description="Email address")
    first_name: Optional[str] = Field(None, max_length=150, description="First name")
    last_name: Optional[str] = Field(None, max_length=150, description="Last name")
    is_active: bool = Field(True, description="Whether user account is active")


class User(UserBase):
    """User schema for API responses."""
    id: int = Field(..., description="User ID")
    date_joined: datetime = Field(..., description="Date user joined")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "date_joined": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-15T10:30:00Z"
            }
        }


class UserProfileBase(BaseModel):
    """Base user profile schema."""
    bio: Optional[str] = Field(None, max_length=500, description="User biography")
    avatar: Optional[str] = Field(None, description="Avatar image URL")
    email_notifications: bool = Field(True, description="Email notification preference")
    show_email_publicly: bool = Field(False, description="Show email publicly")


class UserProfile(UserProfileBase, BaseSchema):
    """User profile schema for API responses."""
    user: User = Field(..., description="Associated user")
    display_name: str = Field(..., description="Display name (full name or username)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "first_name": "John",
                    "last_name": "Doe"
                },
                "bio": "Software developer passionate about web technologies",
                "avatar": "/media/avatars/john.jpg",
                "email_notifications": True,
                "show_email_publicly": False,
                "display_name": "John Doe",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


# =============================================================================
# CONTENT ORGANIZATION SCHEMAS
# =============================================================================

class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., max_length=100, description="Category name")
    slug: str = Field(..., max_length=100, description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Category description")
    icon: Optional[str] = Field(None, max_length=50, description="CSS icon class or emoji")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_active: bool = Field(True, description="Whether category is active")
    sort_order: int = Field(0, description="Sort order for display")


class Category(CategoryBase, BaseSchema):
    """Category schema for API responses."""
    parent: Optional['Category'] = Field(None, description="Parent category")
    subcategories: List['Category'] = Field(default_factory=list, description="Child categories")
    post_count: int = Field(0, description="Number of posts in this category")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Technology",
                "slug": "technology",
                "description": "Posts about technology and programming",
                "icon": "fas fa-laptop-code",
                "color": "#3B82F6",
                "is_active": True,
                "sort_order": 1,
                "parent": None,
                "subcategories": [],
                "post_count": 15,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


class TagBase(BaseModel):
    """Base tag schema."""
    name: str = Field(..., max_length=50, description="Tag name")
    slug: str = Field(..., max_length=50, description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Tag description")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_active: bool = Field(True, description="Whether tag is active")


class Tag(TagBase):
    """Tag schema for API responses."""
    id: int = Field(..., description="Tag ID")
    usage_count: int = Field(0, description="Number of times tag is used")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Python",
                "slug": "python",
                "description": "Python programming language",
                "color": "#3776AB",
                "usage_count": 25,
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }


class PostStatusBase(BaseModel):
    """Base post status schema."""
    name: str = Field(..., max_length=50, description="Status name")
    slug: str = Field(..., max_length=50, description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Status description")
    icon: Optional[str] = Field(None, max_length=50, description="CSS icon class or emoji")
    color: Optional[str] = Field(None, max_length=7, description="Hex color code")
    is_published: bool = Field(False, description="Whether posts with this status are public")
    is_active: bool = Field(True, description="Whether status is active")
    sort_order: int = Field(0, description="Sort order for display")


class PostStatus(PostStatusBase, BaseSchema):
    """Post status schema for API responses."""
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Published",
                "slug": "published",
                "description": "Post is live and visible to public",
                "icon": "fas fa-eye",
                "color": "#10B981",
                "is_published": True,
                "is_active": True,
                "sort_order": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            }
        }


# =============================================================================
# POST SCHEMAS
# =============================================================================

class PostBase(BaseModel):
    """Base post schema."""
    title: str = Field(..., max_length=200, description="Post title")
    slug: str = Field(..., max_length=200, description="URL-friendly slug")
    content: str = Field(..., description="Post content")
    excerpt: Optional[str] = Field(None, max_length=300, description="Post excerpt")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")
    meta_keywords: Optional[str] = Field(None, max_length=255, description="SEO keywords")
    is_featured: bool = Field(False, description="Whether post is featured")
    allow_comments: bool = Field(True, description="Whether comments are allowed")


class PostList(BaseModel):
    """Post schema for list views."""
    id: int = Field(..., description="Post ID")
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL-friendly slug")
    excerpt: Optional[str] = Field(None, description="Post excerpt")
    author: User = Field(..., description="Post author")
    category: Optional[Category] = Field(None, description="Post category")
    tags: List[Tag] = Field(default_factory=list, description="Post tags")
    status: Optional[PostStatus] = Field(None, description="Post status")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    view_count: int = Field(0, description="Number of views")
    like_count: int = Field(0, description="Number of likes")
    comment_count: int = Field(0, description="Number of comments")
    is_featured: bool = Field(False, description="Whether post is featured")
    reading_time: int = Field(1, description="Estimated reading time in minutes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    published_at: Optional[datetime] = Field(None, description="Publication timestamp")

    class Config:
        from_attributes = True


class PostDetail(PostList):
    """Post schema for detail views."""
    content: str = Field(..., description="Full post content")
    meta_description: Optional[str] = Field(None, description="SEO meta description")
    meta_keywords: Optional[str] = Field(None, description="SEO keywords")
    allow_comments: bool = Field(True, description="Whether comments are allowed")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Getting Started with FastAPI",
                "slug": "getting-started-with-fastapi",
                "content": "FastAPI is a modern, fast web framework...",
                "excerpt": "Learn how to build APIs with FastAPI",
                "author": {
                    "id": 1,
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe"
                },
                "category": {
                    "id": 1,
                    "name": "Technology",
                    "slug": "technology"
                },
                "tags": [
                    {"id": 1, "name": "Python", "slug": "python"},
                    {"id": 2, "name": "FastAPI", "slug": "fastapi"}
                ],
                "status": {
                    "id": 1,
                    "name": "Published",
                    "is_published": True
                },
                "view_count": 150,
                "like_count": 25,
                "comment_count": 8,
                "is_featured": True,
                "reading_time": 5,
                "created_at": "2024-01-01T00:00:00Z",
                "published_at": "2024-01-01T12:00:00Z"
            }
        }


# =============================================================================
# ENGAGEMENT SCHEMAS
# =============================================================================

class PostEngagementBase(BaseModel):
    """Base post engagement schema."""
    engagement_type: EngagementType = Field(..., description="Type of engagement")


class PostEngagement(PostEngagementBase):
    """Post engagement schema for API responses."""
    id: int = Field(..., description="Engagement ID")
    user: User = Field(..., description="User who engaged")
    post: PostList = Field(..., description="Post that was engaged with")
    created_at: datetime = Field(..., description="Engagement timestamp")

    class Config:
        from_attributes = True


# =============================================================================
# COMMENT SCHEMAS
# =============================================================================

class CommentBase(BaseModel):
    """Base comment schema."""
    content: str = Field(..., description="Comment content")


class Comment(CommentBase):
    """Comment schema for API responses."""
    id: int = Field(..., description="Comment ID")
    post: PostList = Field(..., description="Post being commented on")
    author: User = Field(..., description="Comment author")
    parent: Optional['Comment'] = Field(None, description="Parent comment for replies")
    is_approved: bool = Field(True, description="Whether comment is approved")
    is_flagged: bool = Field(False, description="Whether comment is flagged")
    like_count: int = Field(0, description="Number of likes")
    replies: List['Comment'] = Field(default_factory=list, description="Comment replies")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class CommentModerationBase(BaseModel):
    """Base comment moderation schema."""
    action: ModerationAction = Field(..., description="Moderation action")
    reason: Optional[str] = Field(None, description="Reason for action")
    notes: Optional[str] = Field(None, description="Internal moderation notes")


class CommentModeration(CommentModerationBase):
    """Comment moderation schema for API responses."""
    id: int = Field(..., description="Moderation ID")
    comment: Comment = Field(..., description="Comment being moderated")
    moderator: User = Field(..., description="Moderator who took action")
    created_at: datetime = Field(..., description="Action timestamp")

    class Config:
        from_attributes = True


class CommentReportBase(BaseModel):
    """Base comment report schema."""
    reason: ReportReason = Field(..., description="Reason for report")
    description: Optional[str] = Field(None, description="Additional report details")


class CommentReport(CommentReportBase):
    """Comment report schema for API responses."""
    id: int = Field(..., description="Report ID")
    comment: Comment = Field(..., description="Comment being reported")
    reporter: User = Field(..., description="User who made the report")
    status: ReportStatus = Field(ReportStatus.pending, description="Report status")
    created_at: datetime = Field(..., description="Report timestamp")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")
    resolved_by: Optional[User] = Field(None, description="User who resolved report")
    resolution_notes: Optional[str] = Field(None, description="Resolution notes")

    class Config:
        from_attributes = True


# =============================================================================
# REQUEST/RESPONSE SCHEMAS
# =============================================================================

class PaginatedResponse(BaseModel):
    """Paginated response schema."""
    count: int = Field(..., description="Total number of items")
    next: Optional[HttpUrl] = Field(None, description="URL for next page")
    previous: Optional[HttpUrl] = Field(None, description="URL for previous page")
    results: List[BaseModel] = Field(..., description="List of items")


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Not found",
                "code": "not_found"
            }
        }


# Update forward references
Category.model_rebuild()
Comment.model_rebuild()