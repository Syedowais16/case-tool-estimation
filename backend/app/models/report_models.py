"""Database Models - Reports, Logs, and ML Models"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Report(Base):
    """Generated estimation reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False)  # estimate, variance, comparison, etc.
    content = Column(Text, nullable=True)  # JSON or HTML content
    format = Column(String(20), default="html")  # html, pdf, json, etc.
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    include_confidence_intervals = Column(Boolean, default=True)
    include_risks = Column(Boolean, default=True)
    include_scenarios = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    file_path = Column(String(500), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="reports")


class AuditLog(Base):
    """Audit trail for compliance and tracking"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)  # create, update, delete, export, etc.
    entity_type = Column(String(100), nullable=False)  # Project, Estimate, etc.
    entity_id = Column(Integer, nullable=False)
    old_values = Column(JSON, nullable=True)  # Previous values if update
    new_values = Column(JSON, nullable=True)  # New values if update
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


class CalibrationModel(Base):
    """Calibration model for historical data analysis"""
    __tablename__ = "calibration_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    model_type = Column(String(100), nullable=False)  # COCOMO, FPA, ML, etc.
    organization = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    
    # Calibration parameters
    calibration_data_count = Column(Integer, nullable=False)  # Number of historical projects used
    accuracy_percentage = Column(Float, nullable=True)  # MAPE - Mean Absolute Percentage Error
    last_calibration_date = Column(DateTime, nullable=True)
    
    # Model coefficients (stored as JSON)
    coefficients = Column(JSON, nullable=True)
    
    # Statistical metrics
    r_squared = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    mae = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MLModel(Base):
    """Machine Learning models for predictions"""
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    model_type = Column(String(100), nullable=False)  # regression, classification, etc.
    algorithm = Column(String(100), nullable=False)  # random_forest, svm, neural_net, etc.
    
    # Model metadata
    training_data_count = Column(Integer, nullable=False)
    feature_count = Column(Integer, nullable=False)
    feature_names = Column(JSON, nullable=True)
    
    # Performance metrics
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    # Model storage
    model_path = Column(String(500), nullable=True)  # Path to saved model file
    model_version = Column(String(50), nullable=True)
    
    # Training info
    training_date = Column(DateTime, nullable=True)
    last_retraining_date = Column(DateTime, nullable=True)
    next_retraining_date = Column(DateTime, nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_production = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Notification(Base):
    """In-app and email notification event."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(80), nullable=False)  # deadline, risk, reminder, review, update
    severity = Column(String(30), default="info")  # info, warning, critical, success
    channel = Column(String(30), default="in_app")  # in_app, email
    is_read = Column(Boolean, default=False)
    due_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    event_metadata = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="notifications")
    project = relationship("Project")


class IntegrationSync(Base):
    """External Jira/Trello sync audit and mapping record."""
    __tablename__ = "integration_syncs"

    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), nullable=False)  # jira, trello
    external_id = Column(String(255), nullable=True)
    external_url = Column(String(500), nullable=True)
    mapped_project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    status = Column(String(50), default="completed")
    task_count = Column(Integer, default=0)
    completed_count = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0)
    payload = Column(JSON, nullable=True)
    imported_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
