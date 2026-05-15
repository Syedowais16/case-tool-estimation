"""Pydantic schemas for Estimations"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class EstimateStatus(str, Enum):
    """Estimate status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    FINAL = "final"


class FunctionPointBase(BaseModel):
    """Base function point schema"""
    ilf_count: int = 0
    ilf_complexity: Optional[str] = None
    eif_count: int = 0
    eif_complexity: Optional[str] = None
    ei_count: int = 0
    ei_complexity: Optional[str] = None
    eo_count: int = 0
    eo_complexity: Optional[str] = None
    eq_count: int = 0
    eq_complexity: Optional[str] = None
    unadjusted_fp: float
    vaf: Optional[float] = None
    adjusted_fp: float


class FunctionPointCreate(FunctionPointBase):
    """Create function point"""
    pass


class FunctionPointResponse(FunctionPointBase):
    """Function point response"""
    id: int
    estimate_id: int
    ilf_contribution: Optional[float]
    eif_contribution: Optional[float]
    ei_contribution: Optional[float]
    eo_contribution: Optional[float]
    eq_contribution: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CostDriverBase(BaseModel):
    """Base cost driver schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    impact_factor: float = Field(..., ge=0.5, le=2.0)
    effort_multiplier: float
    cost_multiplier: float
    duration_multiplier: float = 1.0
    is_active: bool = True


class CostDriverCreate(CostDriverBase):
    """Create cost driver"""
    pass


class CostDriverResponse(CostDriverBase):
    """Cost driver response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class EstimateBase(BaseModel):
    """Base estimate schema"""
    project_id: int
    version_id: int
    estimation_method: str
    estimated_effort_hours: float
    estimated_duration_months: float
    estimated_cost: float
    estimated_team_size: Optional[int] = None
    confidence_level: Optional[int] = None
    confidence_interval_low: Optional[float] = None
    confidence_interval_high: Optional[float] = None
    notes: Optional[str] = None
    assumptions: Optional[str] = None
    risks: Optional[str] = None


class EstimateCreate(EstimateBase):
    """Create estimate"""
    pass


class EstimateUpdate(BaseModel):
    """Update estimate"""
    status: Optional[EstimateStatus] = None
    estimated_effort_hours: Optional[float] = None
    estimated_duration_months: Optional[float] = None
    estimated_cost: Optional[float] = None
    estimated_team_size: Optional[int] = None
    confidence_level: Optional[int] = None
    confidence_interval_low: Optional[float] = None
    confidence_interval_high: Optional[float] = None
    actual_effort_hours: Optional[float] = None
    actual_duration_months: Optional[float] = None
    actual_cost: Optional[float] = None
    actual_team_size: Optional[int] = None
    notes: Optional[str] = None


class EstimateResponse(EstimateBase):
    """Estimate response"""
    id: int
    created_by: int
    status: EstimateStatus
    actual_effort_hours: Optional[float]
    actual_duration_months: Optional[float]
    actual_cost: Optional[float]
    actual_team_size: Optional[int]
    created_at: datetime
    updated_at: datetime
    function_points: List[FunctionPointResponse] = []
    
    class Config:
        from_attributes = True


class HistoricalProjectBase(BaseModel):
    """Base historical project schema"""
    project_name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    project_type: Optional[str] = None
    complexity: Optional[str] = None
    risk_level: Optional[str] = None
    technology_stack: Optional[str] = None
    client_type: Optional[str] = None
    requirement_volatility: Optional[str] = None
    success_status: Optional[str] = None
    team_experience: Optional[str] = None
    estimated_effort_hours: Optional[float] = None
    estimated_duration_months: Optional[float] = None
    estimated_cost: Optional[float] = None
    actual_effort_hours: float
    actual_duration_months: float
    actual_cost: float
    team_size: int
    language: Optional[str] = None
    database_type: Optional[str] = None
    architecture: Optional[str] = None
    scope_description: Optional[str] = None
    productivity: Optional[float] = None
    defect_density: Optional[float] = None
    fpa_unadjusted: Optional[float] = None
    fpa_adjusted: Optional[float] = None
    cocomo_effort: Optional[float] = None
    cocomo_duration: Optional[float] = None
    cocomo_cost: Optional[float] = None
    hybrid_effort: Optional[float] = None
    hybrid_duration: Optional[float] = None
    hybrid_cost: Optional[float] = None
    assumptions: Optional[str] = None
    scenario_summary: Optional[str] = None


class HistoricalProjectCreate(HistoricalProjectBase):
    """Create historical project"""
    pass


class HistoricalProjectResponse(HistoricalProjectBase):
    """Historical project response"""
    id: int
    created_at: datetime
    source: Optional[str]
    
    class Config:
        from_attributes = True


class CocomoCalculationRequest(BaseModel):
    """COCOMO calculation input."""
    size_kloc: float = Field(..., gt=0)
    mode: str = "semi_detached"
    effort_multiplier: float = Field(1.0, gt=0)
    cost_per_person_month: float = Field(9000.0, gt=0)
    risk_level: str = "medium"
    complexity: str = "medium"


class FunctionPointCalculationRequest(BaseModel):
    """Function Point Analysis calculation input."""
    ilf_count: int = Field(0, ge=0)
    ilf_complexity: str = "average"
    eif_count: int = Field(0, ge=0)
    eif_complexity: str = "average"
    ei_count: int = Field(0, ge=0)
    ei_complexity: str = "average"
    eo_count: int = Field(0, ge=0)
    eo_complexity: str = "average"
    eq_count: int = Field(0, ge=0)
    eq_complexity: str = "average"
    value_adjustment_factor: Optional[float] = Field(None, ge=0.65, le=1.35)
    general_system_characteristics: Optional[List[int]] = None
    productivity_fp_per_person_month: float = Field(18.0, gt=0)
    cost_per_person_month: float = Field(9000.0, gt=0)
    risk_level: str = "medium"


class HybridCalculationRequest(BaseModel):
    """Hybrid calculation input."""
    cocomo: CocomoCalculationRequest
    fpa: FunctionPointCalculationRequest
    ml_input: Optional[Dict[str, Any]] = None
    cocomo_weight: float = Field(0.35, ge=0)
    fpa_weight: float = Field(0.40, ge=0)
    ml_weight: float = Field(0.25, ge=0)
    risk_level: str = "medium"
    requirement_volatility: str = "medium"


class MlPredictionRequest(BaseModel):
    """ML prediction input."""
    adjusted_fp: float = Field(120.0, gt=0)
    team_size: int = Field(4, gt=0)
    complexity: str = "medium"
    risk_level: str = "medium"
    requirement_volatility: str = "medium"
    team_experience: str = "mixed"
    architecture: str = "layered"
    productivity: float = Field(1.0, gt=0)
    defect_density: float = Field(2.0, gt=0)
