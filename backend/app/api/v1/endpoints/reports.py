"""Reports and ML Models API endpoints"""
from io import BytesIO
import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.report_models import Report, CalibrationModel, MLModel
from app.schemas.report_schemas import (
    ReportCreate, ReportResponse,
    CalibrationModelCreate, CalibrationModelResponse,
    MLModelCreate, MLModelResponse
)
from app.core.security.security import get_current_user
from app.services.report_export_service import (
    build_project_report_payload,
    render_html_report,
    render_pdf_report,
    render_xlsx_report,
)

router = APIRouter(tags=["reports", "calibration", "ml_models"])


# Report endpoints

@router.post("/reports", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Generate estimation report"""
    new_report = Report(
        **report_data.dict(),
        generated_by=int(current_user["user_id"])
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report


@router.get("/reports/projects/{project_id}/export")
async def export_project_report(
    project_id: int,
    format: str = "pdf",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Download a professional project report as PDF, Excel, HTML, or JSON."""
    try:
        payload = build_project_report_payload(db, project_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error

    safe_name = "".join(character if character.isalnum() else "_" for character in payload["project"]["name"]).strip("_").lower()
    selected_format = format.lower()
    if selected_format == "json":
        return JSONResponse(payload)
    if selected_format == "html":
        return HTMLResponse(render_html_report(payload))
    if selected_format == "xlsx":
        data = render_xlsx_report(payload)
        return StreamingResponse(
            BytesIO(data),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={safe_name}_estimation_report.xlsx"},
        )
    if selected_format == "pdf":
        data = render_pdf_report(payload)
        return StreamingResponse(
            BytesIO(data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={safe_name}_estimation_report.pdf"},
        )

    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="format must be one of: pdf, xlsx, html, json"
    )


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get report by ID"""
    report = db.query(Report).filter(Report.id == report_id).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    return report


@router.get("/projects/{project_id}/reports")
async def list_project_reports(
    project_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List reports for project"""
    total = db.query(Report).filter(Report.project_id == project_id).count()
    reports = db.query(Report).filter(Report.project_id == project_id).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "project_id": project_id,
        "data": reports
    }


@router.delete("/reports/{report_id}")
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete report"""
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    db.delete(report)
    db.commit()

    return {"message": "Report deleted successfully"}


# Calibration Model endpoints

@router.post("/calibration-models", response_model=CalibrationModelResponse)
async def create_calibration_model(
    model_data: CalibrationModelCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create calibration model"""
    new_model = CalibrationModel(**model_data.dict())
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    return new_model


@router.get("/calibration-models/{model_id}", response_model=CalibrationModelResponse)
async def get_calibration_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Get calibration model"""
    model = db.query(CalibrationModel).filter(CalibrationModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calibration model not found"
        )
    
    return model


@router.get("/calibration-models")
async def list_calibration_models(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List calibration models"""
    total = db.query(CalibrationModel).filter(CalibrationModel.is_active == True).count()
    models = db.query(CalibrationModel).filter(CalibrationModel.is_active == True).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": models
    }


# ML Model endpoints

@router.post("/ml-models", response_model=MLModelResponse)
async def create_ml_model(
    model_data: MLModelCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create ML model"""
    new_model = MLModel(**model_data.dict())
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    
    return new_model


@router.get("/ml-models/{model_id}", response_model=MLModelResponse)
async def get_ml_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Get ML model"""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ML model not found"
        )
    
    return model


@router.get("/ml-models")
async def list_ml_models(
    skip: int = 0,
    limit: int = 50,
    is_production: bool = None,
    db: Session = Depends(get_db)
):
    """List ML models"""
    query = db.query(MLModel).filter(MLModel.is_active == True)
    
    if is_production is not None:
        query = query.filter(MLModel.is_production == is_production)
    
    total = query.count()
    models = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": models
    }


@router.put("/ml-models/{model_id}/set-production")
async def set_ml_model_production(
    model_id: int,
    is_production: bool,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Set ML model as production/non-production"""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ML model not found"
        )
    
    model.is_production = is_production
    db.commit()
    db.refresh(model)
    
    return model
