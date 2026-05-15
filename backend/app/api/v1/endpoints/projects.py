"""Project management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.project_models import Project, ProjectVersion
from app.schemas.project_schemas import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectDetailResponse, ProjectVersionCreate
from app.core.security.security import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new project"""
    new_project = Project(
        **project_data.dict(),
        created_by=int(current_user["user_id"])
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    initial_version = ProjectVersion(
        project_id=new_project.id,
        version_number=1,
        description="Initial project version",
        scope=new_project.description,
        assumptions="Initial baseline created during project setup."
    )
    db.add(initial_version)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}


@router.get("")
async def list_projects(
    skip: int = 0,
    limit: int = 50,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List projects (paginated)"""
    query = db.query(Project).filter(Project.is_active == True)
    
    if status_filter:
        query = query.filter(Project.status == status_filter)
    
    total = query.count()
    projects = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": projects
    }


# Project Version endpoints

@router.post("/{project_id}/versions", response_model=dict)
async def create_project_version(
    project_id: int,
    version_data: ProjectVersionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new project version"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    new_version = ProjectVersion(
        project_id=project_id,
        **version_data.dict()
    )
    db.add(new_version)
    db.commit()
    db.refresh(new_version)
    
    return new_version


@router.get("/{project_id}/versions")
async def list_project_versions(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List project versions"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    versions = db.query(ProjectVersion).filter(ProjectVersion.project_id == project_id).all()
    
    return {
        "project_id": project_id,
        "versions": versions
    }
