"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
- ContactMessage -> "contactmessage" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class AuthUser(BaseModel):
    """
    Auth users collection schema
    Collection name: "authuser"
    """
    email: EmailStr = Field(..., description="User email (unique)")
    password_hash: str = Field(..., description="BCrypt password hash")
    name: Optional[str] = Field(None, description="Display name")

class BlogPost(BaseModel):
    """
    Blog posts collection schema
    Collection name: "blogpost"
    """
    title: str = Field(..., description="Post title")
    slug: str = Field(..., description="URL-friendly slug")
    excerpt: Optional[str] = Field(None, description="Short summary")
    content: str = Field(..., description="Markdown or HTML content")
    author: Optional[str] = Field(None, description="Author name")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    published: bool = Field(default=True, description="Publish status")

class ContactMessage(BaseModel):
    """
    Contact messages collection schema
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., description="Message body")

# You can extend with more collections if needed (e.g., TeamMember)
class TeamMember(BaseModel):
    """
    Team members collection schema
    Collection name: "teammember"
    """
    name: str
    role: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
