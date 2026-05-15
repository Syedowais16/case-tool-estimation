"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base, get_db
from app.core.config.settings import Settings
from app.core.security.security import get_password_hash
from app.models.user_models import Role, User

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override get_db for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    """Database fixture"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Test client fixture"""
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


@pytest.fixture
def test_settings():
    """Test settings fixture"""
    settings = Settings(
        debug=True,
        environment="testing",
        database_url=SQLALCHEMY_TEST_DATABASE_URL,
        secret_key="test-secret-key"
    )
    return settings


@pytest.fixture
def test_role(db):
    """Shared test role fixture"""
    role = Role(
        name="test_role",
        description="Test role",
        permissions="test_permission"
    )
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture
def test_user(db, test_role):
    """Shared active test user fixture"""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("password123"),
        role_id=test_role.id,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
