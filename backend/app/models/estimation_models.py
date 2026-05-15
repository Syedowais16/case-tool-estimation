"""Database Models - Estimation and Cost Analysis"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.db.base import Base


class EstimateStatus(str, PyEnum):
    """Estimate status enumeration"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    FINAL = "final"


class Estimate(Base):
    """Software cost estimate model"""
    __tablename__ = "estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    version_id = Column(Integer, ForeignKey("project_versions.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    estimation_method = Column(String(50), nullable=False)  # COCOMO, FP, etc.
    status = Column(Enum(EstimateStatus), default=EstimateStatus.DRAFT)
    
    # Estimate values
    estimated_effort_hours = Column(Float, nullable=False)
    estimated_duration_months = Column(Float, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    estimated_team_size = Column(Integer, nullable=True)
    
    # Confidence metrics
    confidence_level = Column(Integer, nullable=True)  # 0-100
    confidence_interval_low = Column(Float, nullable=True)
    confidence_interval_high = Column(Float, nullable=True)
    
    # Actuals (filled after project completion)
    actual_effort_hours = Column(Float, nullable=True)
    actual_duration_months = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    actual_team_size = Column(Integer, nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    assumptions = Column(Text, nullable=True)
    risks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="estimates")
    version = relationship("ProjectVersion", back_populates="estimates")
    created_by_user = relationship("User", back_populates="estimates")
    function_points = relationship("FunctionPoint", back_populates="estimate", cascade="all, delete-orphan")
    cost_drivers = relationship("CostDriver", secondary="estimate_cost_drivers", back_populates="estimates")
    scale_factors = relationship("ScaleFactor", secondary="estimate_scale_factors", back_populates="estimates")


class HistoricalProject(Base):
    """Historical project data for calibration and comparison"""
    __tablename__ = "historical_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False)
    domain = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    project_type = Column(String(100), nullable=True)
    complexity = Column(String(50), nullable=True)
    risk_level = Column(String(50), nullable=True)
    technology_stack = Column(String(500), nullable=True)
    client_type = Column(String(100), nullable=True)
    requirement_volatility = Column(String(50), nullable=True)
    success_status = Column(String(50), nullable=True)
    team_experience = Column(String(50), nullable=True)  # junior, mid, senior

    # Historical baseline estimates captured before delivery
    estimated_effort_hours = Column(Float, nullable=True)
    estimated_duration_months = Column(Float, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    
    # Historical actual values
    actual_effort_hours = Column(Float, nullable=False)
    actual_duration_months = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=False)
    team_size = Column(Integer, nullable=False)
    
    # Project characteristics
    language = Column(String(100), nullable=True)
    database_type = Column(String(100), nullable=True)
    architecture = Column(String(100), nullable=True)
    scope_description = Column(Text, nullable=True)
    
    # Metrics
    productivity = Column(Float, nullable=True)  # lines of code or function points per hour
    defect_density = Column(Float, nullable=True)  # defects per 1000 lines
    fpa_unadjusted = Column(Float, nullable=True)
    fpa_adjusted = Column(Float, nullable=True)
    cocomo_effort = Column(Float, nullable=True)
    cocomo_duration = Column(Float, nullable=True)
    cocomo_cost = Column(Float, nullable=True)
    hybrid_effort = Column(Float, nullable=True)
    hybrid_duration = Column(Float, nullable=True)
    hybrid_cost = Column(Float, nullable=True)
    assumptions = Column(Text, nullable=True)
    scenario_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String(100), nullable=True)  # internal, industry_data, etc.


class CostDriver(Base):
    """Cost driver/scale factor base model"""
    __tablename__ = "cost_drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # software, hardware, people, process, etc.
    impact_factor = Column(Float, nullable=False)  # 0.5 to 2.0 typical
    effort_multiplier = Column(Float, nullable=False)
    cost_multiplier = Column(Float, nullable=False)
    duration_multiplier = Column(Float, nullable=False, default=1.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships - many to many
    estimates = relationship("Estimate", secondary="estimate_cost_drivers", back_populates="cost_drivers")


class ScaleFactor(Base):
    """Scale factor for cost estimation"""
    __tablename__ = "scale_factors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    factor_value = Column(Float, nullable=False)  # Multiplier value
    factor_type = Column(String(100), nullable=False)  # effort, cost, duration, etc.
    applies_to = Column(String(100), nullable=False)  # project_size, team_experience, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    estimates = relationship("Estimate", secondary="estimate_scale_factors", back_populates="scale_factors")


class FunctionPoint(Base):
    """Function Point Analysis model"""
    __tablename__ = "function_points"
    
    id = Column(Integer, primary_key=True, index=True)
    estimate_id = Column(Integer, ForeignKey("estimates.id"), nullable=False)
    
    # Internal Logical Files (ILF) / Data Functions
    ilf_count = Column(Integer, nullable=False, default=0)
    ilf_complexity = Column(String(20), nullable=True)  # simple, average, complex
    ilf_contribution = Column(Float, nullable=True)
    
    # External Interface Files (EIF)
    eif_count = Column(Integer, nullable=False, default=0)
    eif_complexity = Column(String(20), nullable=True)
    eif_contribution = Column(Float, nullable=True)
    
    # External Inputs (EI)
    ei_count = Column(Integer, nullable=False, default=0)
    ei_complexity = Column(String(20), nullable=True)
    ei_contribution = Column(Float, nullable=True)
    
    # External Outputs (EO)
    eo_count = Column(Integer, nullable=False, default=0)
    eo_complexity = Column(String(20), nullable=True)
    eo_contribution = Column(Float, nullable=True)
    
    # External Inquiries (EQ)
    eq_count = Column(Integer, nullable=False, default=0)
    eq_complexity = Column(String(20), nullable=True)
    eq_contribution = Column(Float, nullable=True)
    
    # Unadjusted Function Points
    unadjusted_fp = Column(Float, nullable=False)
    
    # Value Adjustment Factor (VAF)
    vaf = Column(Float, nullable=True)
    
    # Adjusted Function Points
    adjusted_fp = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    estimate = relationship("Estimate", back_populates="function_points")


# Association tables
from sqlalchemy import Table

estimate_cost_drivers = Table(
    'estimate_cost_drivers',
    Base.metadata,
    Column('estimate_id', Integer, ForeignKey('estimates.id'), primary_key=True),
    Column('cost_driver_id', Integer, ForeignKey('cost_drivers.id'), primary_key=True)
)

estimate_scale_factors = Table(
    'estimate_scale_factors',
    Base.metadata,
    Column('estimate_id', Integer, ForeignKey('estimates.id'), primary_key=True),
    Column('scale_factor_id', Integer, ForeignKey('scale_factors.id'), primary_key=True)
)
