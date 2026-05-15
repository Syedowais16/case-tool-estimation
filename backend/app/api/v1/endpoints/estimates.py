"""Estimation API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.estimation_models import Estimate, CostDriver, ScaleFactor, FunctionPoint, HistoricalProject
from app.schemas.estimate_schemas import (
    EstimateCreate, EstimateResponse, EstimateUpdate, CostDriverCreate, CostDriverResponse,
    FunctionPointCreate, FunctionPointResponse, HistoricalProjectCreate, HistoricalProjectResponse,
    CocomoCalculationRequest, FunctionPointCalculationRequest, HybridCalculationRequest, MlPredictionRequest
)
from app.core.security.security import get_current_user
from app.services.estimation_engine import (
    calculate_cocomo,
    calculate_fpa,
    calculate_hybrid,
    build_ml_insights,
    predict_with_ml,
)

router = APIRouter(prefix="/estimates", tags=["estimates"])


def _calculation_error(error: ValueError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=str(error)
    )


@router.post("/calculate/cocomo")
async def calculate_cocomo_estimate(
    request: CocomoCalculationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Calculate a COCOMO estimate without saving it."""
    try:
        return calculate_cocomo(**request.dict())
    except ValueError as error:
        raise _calculation_error(error) from error


@router.post("/calculate/fpa")
async def calculate_function_point_estimate(
    request: FunctionPointCalculationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Calculate Function Point Analysis without saving it."""
    try:
        return calculate_fpa(**request.dict())
    except ValueError as error:
        raise _calculation_error(error) from error


@router.post("/calculate/hybrid")
async def calculate_hybrid_estimate(
    request: HybridCalculationRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Calculate a hybrid COCOMO + FPA + optional ML estimate."""
    try:
        cocomo_result = calculate_cocomo(**request.cocomo.dict())
        fpa_result = calculate_fpa(**request.fpa.dict())
        ml_result = None
        if request.ml_input:
            historical_projects = db.query(HistoricalProject).all()
            ml_result = predict_with_ml(request.ml_input, historical_projects)
        return calculate_hybrid(
            cocomo_result=cocomo_result,
            fpa_result=fpa_result,
            ml_result=ml_result,
            cocomo_weight=request.cocomo_weight,
            fpa_weight=request.fpa_weight,
            ml_weight=request.ml_weight,
            risk_level=request.risk_level,
            requirement_volatility=request.requirement_volatility,
        )
    except ValueError as error:
        raise _calculation_error(error) from error


@router.post("/ml/predict")
async def predict_ml_estimate(
    request: MlPredictionRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Train on historical projects and predict effort, duration, and cost."""
    historical_projects = db.query(HistoricalProject).all()
    try:
        return predict_with_ml(request.dict(), historical_projects)
    except ValueError as error:
        raise _calculation_error(error) from error


@router.get("/ml/insights")
async def get_ml_insights(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Return model quality and feature-importance insights."""
    historical_projects = db.query(HistoricalProject).all()
    return build_ml_insights(historical_projects)


@router.post("/", response_model=EstimateResponse)
async def create_estimate(
    estimate_data: EstimateCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new software cost estimate"""
    new_estimate = Estimate(
        **estimate_data.dict(),
        created_by=int(current_user["user_id"])
    )
    db.add(new_estimate)
    db.commit()
    db.refresh(new_estimate)
    
    return new_estimate


@router.get("/project/{project_id}")
async def list_estimates_by_project(
    project_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List estimates for a project"""
    total = db.query(Estimate).filter(Estimate.project_id == project_id).count()
    estimates = db.query(Estimate).filter(Estimate.project_id == project_id).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "project_id": project_id,
        "data": estimates
    }


# Cost Driver endpoints

@router.post("/cost-drivers", response_model=CostDriverResponse)
async def create_cost_driver(
    driver_data: CostDriverCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create cost driver"""
    new_driver = CostDriver(**driver_data.dict())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    return new_driver


@router.get("/cost-drivers/{driver_id}", response_model=CostDriverResponse)
async def get_cost_driver(driver_id: int, db: Session = Depends(get_db)):
    """Get cost driver"""
    driver = db.query(CostDriver).filter(CostDriver.id == driver_id).first()
    
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost driver not found"
        )
    
    return driver


@router.get("/cost-drivers")
async def list_cost_drivers(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List cost drivers"""
    total = db.query(CostDriver).filter(CostDriver.is_active == True).count()
    drivers = db.query(CostDriver).filter(CostDriver.is_active == True).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": drivers
    }


# Function Points endpoints

@router.post("/{estimate_id}/function-points", response_model=FunctionPointResponse)
async def create_function_points(
    estimate_id: int,
    fp_data: FunctionPointCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create function point analysis"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    
    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estimate not found"
        )

    fp_payload = fp_data.dict()
    try:
        calculated_fp = calculate_fpa(
            ilf_count=fp_data.ilf_count,
            ilf_complexity=fp_data.ilf_complexity or "average",
            eif_count=fp_data.eif_count,
            eif_complexity=fp_data.eif_complexity or "average",
            ei_count=fp_data.ei_count,
            ei_complexity=fp_data.ei_complexity or "average",
            eo_count=fp_data.eo_count,
            eo_complexity=fp_data.eo_complexity or "average",
            eq_count=fp_data.eq_count,
            eq_complexity=fp_data.eq_complexity or "average",
            value_adjustment_factor=fp_data.vaf,
        )
        fp_payload.update({
            "ilf_contribution": calculated_fp["ilf_contribution"],
            "eif_contribution": calculated_fp["eif_contribution"],
            "ei_contribution": calculated_fp["ei_contribution"],
            "eo_contribution": calculated_fp["eo_contribution"],
            "eq_contribution": calculated_fp["eq_contribution"],
            "unadjusted_fp": calculated_fp["unadjusted_fp"],
            "vaf": calculated_fp["vaf"],
            "adjusted_fp": calculated_fp["adjusted_fp"],
        })
    except ValueError as error:
        raise _calculation_error(error) from error

    new_fp = FunctionPoint(
        estimate_id=estimate_id,
        **fp_payload
    )
    db.add(new_fp)
    db.commit()
    db.refresh(new_fp)
    
    return new_fp


@router.get("/{estimate_id}/function-points")
async def get_function_points(
    estimate_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get function points for estimate"""
    fps = db.query(FunctionPoint).filter(FunctionPoint.estimate_id == estimate_id).all()
    
    return {
        "estimate_id": estimate_id,
        "function_points": fps
    }


# Historical Projects endpoints

@router.post("/historical-projects", response_model=HistoricalProjectResponse)
async def create_historical_project(
    project_data: HistoricalProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add historical project for calibration"""
    new_project = HistoricalProject(**project_data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.get("/historical-projects")
async def list_historical_projects(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List historical projects"""
    total = db.query(HistoricalProject).count()
    projects = db.query(HistoricalProject).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": projects
    }


@router.get("/{estimate_id}", response_model=EstimateResponse)
async def get_estimate(
    estimate_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get estimate by ID"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    
    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estimate not found"
        )
    
    return estimate


@router.put("/{estimate_id}", response_model=EstimateResponse)
async def update_estimate(
    estimate_id: int,
    estimate_data: EstimateUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update estimate"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()
    
    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estimate not found"
        )
    
    update_data = estimate_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(estimate, field, value)
    
    db.commit()
    db.refresh(estimate)
    
    return estimate


@router.delete("/{estimate_id}")
async def delete_estimate(
    estimate_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete estimate"""
    estimate = db.query(Estimate).filter(Estimate.id == estimate_id).first()

    if not estimate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estimate not found"
        )

    db.delete(estimate)
    db.commit()

    return {"message": "Estimate deleted successfully"}
