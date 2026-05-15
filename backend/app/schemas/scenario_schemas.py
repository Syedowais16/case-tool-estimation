"""Pydantic schemas for Scenarios, Risks, and Resources"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ScenarioBase(BaseModel):
    """Base scenario schema"""
    project_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    scenario_type: str  # optimistic, pessimistic, realistic, custom
    effort_adjustment: float = 1.0
    duration_adjustment: float = 1.0
    cost_adjustment: float = 1.0
    team_size_adjustment: float = 1.0


class ScenarioCreate(ScenarioBase):
    """Create scenario"""
    pass


class ScenarioUpdate(BaseModel):
    """Update scenario"""
    name: Optional[str] = None
    description: Optional[str] = None
    scenario_type: Optional[str] = None
    effort_adjustment: Optional[float] = None
    duration_adjustment: Optional[float] = None
    cost_adjustment: Optional[float] = None
    team_size_adjustment: Optional[float] = None


class ScenarioResponse(ScenarioBase):
    """Scenario response"""
    id: int
    estimated_effort: Optional[float]
    estimated_duration: Optional[float]
    estimated_cost: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RiskBase(BaseModel):
    """Base risk schema"""
    project_id: int
    description: str
    category: str
    probability: float = Field(..., ge=0, le=1)
    impact: float = Field(..., ge=0, le=1)
    mitigation_strategy: Optional[str] = None
    owner: Optional[str] = None
    status: str = "active"
    effort_contingency: float = 0
    cost_contingency: float = 0


class RiskCreate(RiskBase):
    """Create risk"""
    pass


class RiskUpdate(BaseModel):
    """Update risk"""
    description: Optional[str] = None
    category: Optional[str] = None
    probability: Optional[float] = None
    impact: Optional[float] = None
    mitigation_strategy: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    effort_contingency: Optional[float] = None
    cost_contingency: Optional[float] = None


class RiskResponse(RiskBase):
    """Risk response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    """Base resource schema"""
    project_id: int
    user_id: int
    role: str
    allocation_percentage: float = Field(..., ge=0, le=100)
    hourly_rate: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skills: Optional[str] = None
    availability: str = "available"


class ResourceCreate(ResourceBase):
    """Create resource"""
    pass


class ResourceUpdate(BaseModel):
    """Update resource"""
    role: Optional[str] = None
    allocation_percentage: Optional[float] = None
    hourly_rate: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skills: Optional[str] = None
    availability: Optional[str] = None


class ResourceResponse(ResourceBase):
    """Resource response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
