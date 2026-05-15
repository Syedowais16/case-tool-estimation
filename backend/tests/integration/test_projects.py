"""Project creation and management tests"""
import pytest
from app.models.project_models import Project


@pytest.fixture
def auth_headers(client, test_user):
    """Get auth headers for test user"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_project(client, auth_headers, test_user):
    """Test project creation"""
    response = client.post(
        "/api/v1/projects",
        headers=auth_headers,
        json={
            "name": "Test Project",
            "description": "A test project",
            "budget": 50000.00,
            "team_size": 5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["created_by"] == test_user.id


def test_get_projects(client, auth_headers, test_user, db):
    """Test getting projects list"""
    # Create a test project
    project = Project(
        name="Test Project",
        description="Test",
        created_by=test_user.id,
        budget=50000.00
    )
    db.add(project)
    db.commit()
    
    response = client.get(
        "/api/v1/projects",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["data"]) >= 1


def test_get_project(client, auth_headers, test_user, db):
    """Test getting single project"""
    project = Project(
        name="Test Project",
        created_by=test_user.id
    )
    db.add(project)
    db.commit()
    
    response = client.get(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"


def test_update_project(client, auth_headers, test_user, db):
    """Test project update"""
    project = Project(
        name="Original Name",
        created_by=test_user.id
    )
    db.add(project)
    db.commit()
    
    response = client.put(
        f"/api/v1/projects/{project.id}",
        headers=auth_headers,
        json={"name": "Updated Name"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


def test_delete_project(client, auth_headers, test_user, db):
    """Test project deletion"""
    project = Project(
        name="To Delete",
        created_by=test_user.id
    )
    db.add(project)
    db.commit()
    project_id = project.id
    
    response = client.delete(
        f"/api/v1/projects/{project_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(
        f"/api/v1/projects/{project_id}",
        headers=auth_headers
    )
    assert response.status_code == 404
