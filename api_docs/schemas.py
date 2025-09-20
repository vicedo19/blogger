"""
Pydantic schemas for FastAPI documentation.

This module contains Pydantic models that mirror the Django models
and serializers to provide comprehensive API documentation through
FastAPI's automatic OpenAPI/Swagger UI generation.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class UserSchema(BaseModel):
    """User schema for API documentation."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str = Field(..., description="Unique username")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    email: str = Field(..., description="User's email address")


class PostStatusSchema(BaseModel):
    """Post status schema for API documentation."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str = Field(..., description="Status name (e.g., 'Published', 'Draft')")
    slug: str = Field(..., description="URL-friendly status identifier")
    description: Optional[str] = Field(None, description="Status description")
    icon: Optional[str] = Field(None, description="CSS icon class or emoji")
    color: Optional[str] = Field(None, description="Hex color code for UI display")
    is_published: bool = Field(..., description="Whether posts with this status are publicly visible")
    is_active: bool = Field(..., description="Whether this status is currently active")
    sort_order: int = Field(..., description="Display order for status options")
    created_at: datetime = Field(..., description="Status creation timestamp")
    updated_at: datetime = Field(..., description="Status last update timestamp")


class CategorySchema(BaseModel):
    """Category schema for API documentation."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str = Field(..., max_length=100, description="Category name")
    slug: str = Field(..., max_length=100, description="URL-friendly category identifier")
    description: Optional[str] = Field(None, description="Category description")
    post_count: int = Field(..., description="Number of published posts in this category")
    created_at: datetime = Field(..., description="Category creation timestamp")
    updated_at: datetime = Field(..., description="Category last update timestamp")


class TagSchema(BaseModel):
    """Tag schema for API documentation."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str = Field(..., max_length=50, description="Tag name")
    slug: str = Field(..., max_length=50, description="URL-friendly tag identifier")
    post_count: int = Field(..., description="Number of published posts with this tag")
    created_at: datetime = Field(..., description="Tag creation timestamp")


class PostListSchema(BaseModel):
    """Post list schema for API documentation (minimal fields)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str = Field(..., max_length=200, description="Post title")
    slug: str = Field(..., max_length=200, description="URL-friendly post identifier")
    author: UserSchema = Field(..., description="Post author information")
    excerpt: Optional[str] = Field(None, max_length=300, description="Post excerpt/summary")
    category: Optional[CategorySchema] = Field(None, description="Post category")
    tags: List[TagSchema] = Field(default=[], description="Post tags")
    status: Optional[PostStatusSchema] = Field(None, description="Post status")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    reading_time: int = Field(..., description="Estimated reading time in minutes")
    created_at: datetime = Field(..., description="Post creation timestamp")
    updated_at: datetime = Field(..., description="Post last update timestamp")
    published_at: Optional[datetime] = Field(None, description="Post publication timestamp")


class PostDetailSchema(BaseModel):
    """Post detail schema for API documentation (all fields)."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str = Field(..., max_length=200, description="Post title")
    slug: str = Field(..., max_length=200, description="URL-friendly post identifier")
    author: UserSchema = Field(..., description="Post author information")
    content: str = Field(..., description="Full post content")
    excerpt: Optional[str] = Field(None, max_length=300, description="Post excerpt/summary")
    category: Optional[CategorySchema] = Field(None, description="Post category")
    tags: List[TagSchema] = Field(default=[], description="Post tags")
    status: Optional[PostStatusSchema] = Field(None, description="Post status")
    featured_image: Optional[str] = Field(None, description="Featured image URL")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")
    reading_time: int = Field(..., description="Estimated reading time in minutes")
    created_at: datetime = Field(..., description="Post creation timestamp")
    updated_at: datetime = Field(..., description="Post last update timestamp")
    published_at: Optional[datetime] = Field(None, description="Post publication timestamp")


class CommentSchema(BaseModel):
    """Comment schema for API documentation."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    post: int = Field(..., description="ID of the post this comment belongs to")
    author: UserSchema = Field(..., description="Comment author information")
    content: str = Field(..., description="Comment content")
    parent: Optional[int] = Field(None, description="ID of parent comment for threaded comments")
    is_approved: bool = Field(..., description="Whether the comment is approved for display")
    created_at: datetime = Field(..., description="Comment creation timestamp")
    updated_at: datetime = Field(..., description="Comment last update timestamp")
    replies: List['CommentSchema'] = Field(default=[], description="Nested replies to this comment")


class PaginatedResponse(BaseModel):
    """Paginated response schema for list endpoints."""
    model_config = ConfigDict(from_attributes=True)
    
    count: int = Field(..., description="Total number of items")
    next: Optional[str] = Field(None, description="URL for next page")
    previous: Optional[str] = Field(None, description="URL for previous page")
    results: List[BaseModel] = Field(..., description="List of items for current page")


class PaginatedPostListResponse(PaginatedResponse):
    """Paginated response for post list endpoints."""
    results: List[PostListSchema] = Field(..., description="List of posts for current page")


class PaginatedCommentListResponse(PaginatedResponse):
    """Paginated response for comment list endpoints."""
    results: List[CommentSchema] = Field(..., description="List of comments for current page")


class PaginatedCategoryListResponse(PaginatedResponse):
    """Paginated response for category list endpoints."""
    results: List[CategorySchema] = Field(..., description="List of categories for current page")


class PaginatedTagListResponse(PaginatedResponse):
    """Paginated response for tag list endpoints."""
    results: List[TagSchema] = Field(..., description="List of tags for current page")


class ErrorResponse(BaseModel):
    """Error response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    detail: str = Field(..., description="Error message")
    code: Optional[str] = Field(None, description="Error code")


class ValidationErrorResponse(BaseModel):
    """Validation error response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    field_name: List[str] = Field(..., description="List of validation errors for this field")


# Create request schemas for POST/PUT operations
class PostCreateSchema(BaseModel):
    """Schema for creating a new post."""
    model_config = ConfigDict(from_attributes=True)
    
    title: str = Field(..., max_length=200, description="Post title")
    slug: str = Field(..., max_length=200, description="URL-friendly post identifier")
    content: str = Field(..., description="Full post content")
    excerpt: Optional[str] = Field(None, max_length=300, description="Post excerpt/summary")
    category: Optional[int] = Field(None, description="Category ID")
    tags: List[int] = Field(default=[], description="List of tag IDs")
    status: Optional[int] = Field(None, description="Status ID")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")


class CommentCreateSchema(BaseModel):
    """Schema for creating a new comment."""
    model_config = ConfigDict(from_attributes=True)
    
    post: int = Field(..., description="ID of the post to comment on")
    content: str = Field(..., description="Comment content")
    parent: Optional[int] = Field(None, description="ID of parent comment for replies")


class CategoryCreateSchema(BaseModel):
    """Schema for creating a new category."""
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=100, description="Category name")
    slug: str = Field(..., max_length=100, description="URL-friendly category identifier")
    description: Optional[str] = Field(None, description="Category description")


class TagCreateSchema(BaseModel):
    """Schema for creating a new tag."""
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=50, description="Tag name")
    slug: str = Field(..., max_length=50, description="URL-friendly tag identifier")