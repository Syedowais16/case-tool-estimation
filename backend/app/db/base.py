"""Database Base and Session Management"""
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config.settings import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    poolclass=QueuePool,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create SessionLocal
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create declarative base
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _ensure_sqlite_columns() -> None:
    """Apply lightweight SQLite schema upgrades for AI-generated starter databases."""
    if engine.dialect.name != "sqlite":
        return

    required_columns = {
        "domain": "VARCHAR(100)",
        "complexity": "VARCHAR(50)",
        "risk_level": "VARCHAR(50)",
        "technology_stack": "VARCHAR(500)",
        "client_type": "VARCHAR(100)",
        "requirement_volatility": "VARCHAR(50)",
        "success_status": "VARCHAR(50)",
        "estimated_effort_hours": "FLOAT",
        "estimated_duration_months": "FLOAT",
        "estimated_cost": "FLOAT",
        "fpa_unadjusted": "FLOAT",
        "fpa_adjusted": "FLOAT",
        "cocomo_effort": "FLOAT",
        "cocomo_duration": "FLOAT",
        "cocomo_cost": "FLOAT",
        "hybrid_effort": "FLOAT",
        "hybrid_duration": "FLOAT",
        "hybrid_cost": "FLOAT",
        "assumptions": "TEXT",
        "scenario_summary": "TEXT",
    }

    inspector = inspect(engine)
    if "historical_projects" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("historical_projects")}
    with engine.begin() as connection:
        for column_name, column_type in required_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE historical_projects ADD COLUMN {column_name} {column_type}"))


def init_db() -> None:
    """Initialize database with all tables"""
    from app.models.all_models import (
        User, Role, Project, ProjectVersion, Estimate,
        HistoricalProject, CostDriver, ScaleFactor, FunctionPoint,
        Scenario, Risk, Resource, Report, AuditLog, CalibrationModel, MLModel,
        Notification, IntegrationSync
    )
    from app.core.security.security import get_password_hash
    from app.db.seed_data import seed_demo_portfolio
    
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns()

    db = SessionLocal()
    try:
        if db.query(Role).count() == 0:
            db.add_all([
                Role(
                    name="Administrator",
                    description="Full platform access",
                    permissions="*"
                ),
                Role(
                    name="Project Manager",
                    description="Manage projects, estimates, and reports",
                    permissions="projects,estimates,reports,resources,risks,scenarios"
                ),
                Role(
                    name="Estimator",
                    description="Create estimates and supporting analysis",
                    permissions="projects,estimates,reports,scenarios,risks"
                ),
                Role(
                    name="Analyst",
                    description="Read insights and maintain reference data",
                    permissions="reports,historical_projects,cost_drivers,ml_models"
                ),
            ])
            db.commit()

        admin_role = db.query(Role).filter(Role.name == "Administrator").first()
        if admin_role and db.query(User).count() == 0:
            db.add(
                User(
                    email="admin@example.com",
                    username="admin",
                    full_name="CASE Tool Administrator",
                    hashed_password=get_password_hash("admin123"),
                    role_id=admin_role.id,
                    is_active=True,
                    is_verified=True,
                    organization="CASE Tool",
                    department="Platform",
                )
            )
            db.commit()

        seed_demo_portfolio(db)
    finally:
        db.close()


def drop_db() -> None:
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
