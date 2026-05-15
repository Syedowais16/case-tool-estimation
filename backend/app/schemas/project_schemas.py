"""Pydantic schemas for Projects"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ProjectStatus(str, Enum):
    """Project status"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ON_HOLD = "on_hold"


class ProjectVersionBase(BaseModel):
    """Base project version schema"""
    version_number: int
    description: Optional[str] = None
    scope: Optional[str] = None
    assumptions: Optional[str] = None
    constraints: Optional[str] = None


class ProjectVersionCreate(ProjectVersionBase):
    """Create project version"""
    pass


class ProjectVersionResponse(ProjectVersionBase):
    """Project version response"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    team_size: Optional[int] = None
    client_name: Optional[str] = None
    project_manager: Optional[str] = None
    department: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Create project schema"""
    pass


class ProjectUpdate(BaseModel):
    """Update project schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    team_size: Optional[int] = None
    client_name: Optional[str] = None
    project_manager: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    versions: List[ProjectVersionResponse] = []
    
    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    """Detailed project response with all relations"""
    pass
