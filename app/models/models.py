from pydantic import BaseModel, Field
from datetime import datetime

# User Models (Example 1)
class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: str = Field(..., description="User email address")
    full_name: str | None = Field(None, description="Optional full name")

class UserResponse(BaseModel):
    """Model for user response"""
    id: int
    username: str
    email: str
    full_name: str | None = None
    created_at: datetime

class UserUpdate(BaseModel):
    """Model for updating user information"""
    email: str | None = None
    full_name: str | None = None

# Product Models (Example 2)
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    in_stock: bool = True

class ProductCreate(ProductBase):
    """Model for creating a product"""
    pass

class ProductResponse(ProductBase):
    """Model for product response"""
    id: int
    created_at: datetime

class ProductUpdate(BaseModel):
    """Model for updating a product"""
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    in_stock: bool | None = None