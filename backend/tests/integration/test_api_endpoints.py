"""Integration tests for API endpoints"""
import pytest
from app.models.user_models import User, Role
from app.core.security.security import get_password_hash


@pytest.fixture
def test_role(db):
    """Create test role"""
    role = Role(
        name="test_role",
        description="Test role",
        permissions="test_permission"
    )
    db.add(role)
    db.commit()
    return role


@pytest.fixture
def test_user(db, test_role):
    """Create test user"""
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
    return user


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure_wrong_password(client, test_user):
    """Test login failure with wrong password"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


def test_login_failure_nonexistent_user(client):
    """Test login failure with nonexistent user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401


def test_register_user(client, test_role, db):
    """Test user registration"""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "password123",
            "role_id": test_role.id
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"


def test_register_duplicate_email(client, test_user, test_role):
    """Test registration with duplicate email"""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "test@example.com",  # Already exists
            "username": "newuser",
            "full_name": "New User",
            "password": "password123",
            "role_id": test_role.id
        }
    )
    
    assert response.status_code == 400


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
