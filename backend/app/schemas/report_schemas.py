"""Pydantic schemas for Reports and Utilities"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


class ReportBase(BaseModel):
    """Base report schema"""
    project_id: int
    title: str = Field(..., min_length=1, max_length=255)
    report_type: str
    content: Optional[str] = None
    format: str = "html"
    include_confidence_intervals: bool = True
    include_risks: bool = True
    include_scenarios: bool = True


class ReportCreate(ReportBase):
    """Create report"""
    pass


class ReportResponse(ReportBase):
    """Report response"""
    id: int
    generated_by: Optional[int]
    created_at: datetime
    file_path: Optional[str]
    
    class Config:
        from_attributes = True


class AuditLogResponse(BaseModel):
    """Audit log response"""
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class CalibrationModelBase(BaseModel):
    """Base calibration model schema"""
    name: str = Field(..., min_length=1, max_length=255, unique=True)
    description: Optional[str] = None
    model_type: str
    organization: Optional[str] = None
    industry: Optional[str] = None
    calibration_data_count: int
    accuracy_percentage: Optional[float] = None
    is_active: bool = True


class CalibrationModelCreate(CalibrationModelBase):
    """Create calibration model"""
    coefficients: Optional[Dict[str, Any]] = None


class CalibrationModelResponse(CalibrationModelBase):
    """Calibration model response"""
    id: int
    coefficients: Optional[Dict[str, Any]]
    r_squared: Optional[float]
    rmse: Optional[float]
    mae: Optional[float]
    last_calibration_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MLModelBase(BaseModel):
    """Base ML model schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    model_type: str
    algorithm: str
    training_data_count: int
    feature_count: int
    feature_names: Optional[List[str]] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    is_active: bool = True
    is_production: bool = False


class MLModelCreate(MLModelBase):
    """Create ML model"""
    pass


class MLModelResponse(MLModelBase):
    """ML model response"""
    id: int
    model_version: Optional[str]
    training_date: Optional[datetime]
    last_retraining_date: Optional[datetime]
    next_retraining_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    """Pagination parameters"""
    skip: int = Field(0, ge=0)
    limit: int = Field(50, ge=1, le=1000)


class ListResponse(BaseModel):
    """Generic list response"""
    total: int
    skip: int
    limit: int
    data: List[Any]


class ErrorResponse(BaseModel):
    """Error response"""
    status_code: int
    message: str
    details: Optional[Dict[str, Any]] = None
