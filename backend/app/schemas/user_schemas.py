"""Pydantic schemas for User and Authentication"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class RoleBase(BaseModel):
    """Base role schema"""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[str] = None
    is_active: bool = True


class RoleCreate(RoleBase):
    """Create role schema"""
    pass


class RoleUpdate(BaseModel):
    """Update role schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[str] = None
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    """Role response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None


class UserCreate(UserBase):
    """Create user schema"""
    password: str = Field(..., min_length=8, max_length=100)
    role_id: int


class UserUpdate(BaseModel):
    """Update user schema"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    organization: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    role_id: int
    is_active: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserWithRole(UserResponse):
    """User response with role"""
    role: RoleResponse


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
