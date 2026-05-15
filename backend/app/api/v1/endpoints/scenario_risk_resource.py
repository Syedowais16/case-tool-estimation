"""Scenarios, Risks, and Resources API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.scenario_models import Scenario, Risk, Resource
from app.schemas.scenario_schemas import (
    ScenarioCreate, ScenarioResponse, ScenarioUpdate,
    RiskCreate, RiskResponse, RiskUpdate,
    ResourceCreate, ResourceResponse, ResourceUpdate
)
from app.core.security.security import get_current_user

router = APIRouter(tags=["scenarios", "risks", "resources"])


# Scenario endpoints

@router.post("/scenarios", response_model=ScenarioResponse)
async def create_scenario(
    scenario_data: ScenarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create what-if scenario"""
    new_scenario = Scenario(**scenario_data.dict())
    db.add(new_scenario)
    db.commit()
    db.refresh(new_scenario)
    
    return new_scenario


@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get scenario by ID"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    return scenario


@router.put("/scenarios/{scenario_id}", response_model=ScenarioResponse)
async def update_scenario(
    scenario_id: int,
    scenario_data: ScenarioUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update scenario"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )
    
    update_data = scenario_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scenario, field, value)
    
    db.commit()
    db.refresh(scenario)
    
    return scenario


@router.get("/projects/{project_id}/scenarios")
async def list_project_scenarios(
    project_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List scenarios for project"""
    total = db.query(Scenario).filter(Scenario.project_id == project_id).count()
    scenarios = db.query(Scenario).filter(Scenario.project_id == project_id).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "project_id": project_id,
        "data": scenarios
    }


@router.delete("/scenarios/{scenario_id}")
async def delete_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete scenario"""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()

    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scenario not found"
        )

    db.delete(scenario)
    db.commit()

    return {"message": "Scenario deleted successfully"}


# Risk endpoints

@router.post("/risks", response_model=RiskResponse)
async def create_risk(
    risk_data: RiskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create project risk"""
    new_risk = Risk(**risk_data.dict())
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)
    
    return new_risk


@router.get("/risks/{risk_id}", response_model=RiskResponse)
async def get_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get risk by ID"""
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )
    
    return risk


@router.put("/risks/{risk_id}", response_model=RiskResponse)
async def update_risk(
    risk_id: int,
    risk_data: RiskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update risk"""
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    
    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )
    
    update_data = risk_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(risk, field, value)
    
    db.commit()
    db.refresh(risk)
    
    return risk


@router.get("/projects/{project_id}/risks")
async def list_project_risks(
    project_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List risks for project"""
    total = db.query(Risk).filter(Risk.project_id == project_id).count()
    risks = db.query(Risk).filter(Risk.project_id == project_id).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "project_id": project_id,
        "data": risks
    }


@router.delete("/risks/{risk_id}")
async def delete_risk(
    risk_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete risk"""
    risk = db.query(Risk).filter(Risk.id == risk_id).first()

    if not risk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk not found"
        )

    db.delete(risk)
    db.commit()

    return {"message": "Risk deleted successfully"}


# Resource endpoints

@router.post("/resources", response_model=ResourceResponse)
async def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Allocate resource to project"""
    new_resource = Resource(**resource_data.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    
    return new_resource


@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get resource by ID"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return resource


@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update resource"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    update_data = resource_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)
    
    db.commit()
    db.refresh(resource)
    
    return resource


@router.get("/projects/{project_id}/resources")
async def list_project_resources(
    project_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List resources for project"""
    total = db.query(Resource).filter(Resource.project_id == project_id).count()
    resources = db.query(Resource).filter(Resource.project_id == project_id).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "project_id": project_id,
        "data": resources
    }


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete resource"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    db.delete(resource)
    db.commit()

    return {"message": "Resource deleted successfully"}
