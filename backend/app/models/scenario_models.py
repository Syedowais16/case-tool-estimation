"""Database Models - Scenarios, Risks, and Resources"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Scenario(Base):
    """What-if scenario for sensitivity analysis"""
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scenario_type = Column(String(50), nullable=False)  # optimistic, pessimistic, realistic, custom
    
    # Parameter adjustments
    effort_adjustment = Column(Float, default=1.0)  # multiplier
    duration_adjustment = Column(Float, default=1.0)
    cost_adjustment = Column(Float, default=1.0)
    team_size_adjustment = Column(Float, default=1.0)
    
    # Results
    estimated_effort = Column(Float, nullable=True)
    estimated_duration = Column(Float, nullable=True)
    estimated_cost = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="scenarios")


class Risk(Base):
    """Risk identification and mitigation"""
    __tablename__ = "risks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # technical, schedule, resource, etc.
    probability = Column(Float, nullable=False)  # 0-1 scale
    impact = Column(Float, nullable=False)  # 0-1 scale or 1-5 scale
    mitigation_strategy = Column(Text, nullable=True)
    owner = Column(String(255), nullable=True)
    status = Column(String(50), default="active")  # active, mitigated, accepted, avoided
    effort_contingency = Column(Float, default=0)  # hours
    cost_contingency = Column(Float, default=0)  # currency amount
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="risks")


class Resource(Base):
    """Project resource allocation"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(100), nullable=False)  # developer, analyst, architect, qa, etc.
    allocation_percentage = Column(Float, nullable=False)  # 0-100
    hourly_rate = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    skills = Column(Text, nullable=True)  # comma-separated or JSON
    availability = Column(String(50), default="available")  # available, busy, unavailable
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="resources")
    user = relationship("User", back_populates="resources")
