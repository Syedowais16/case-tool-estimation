"""Advanced dashboard analytics endpoints."""
from collections import Counter, defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security.security import get_current_user
from app.db.base import get_db
from app.models.estimation_models import Estimate, HistoricalProject
from app.models.project_models import Project
from app.models.report_models import Report
from app.models.scenario_models import Resource, Risk, Scenario
from app.services.estimation_engine import build_ml_insights

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _safe(value, default=0):
    return value if value is not None else default


@router.get("/analytics")
async def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Return dynamic portfolio, estimation, ML, risk, and productivity analytics."""
    projects = db.query(Project).filter(Project.is_active == True).all()
    estimates = db.query(Estimate).all()
    historical_projects = db.query(HistoricalProject).all()
    risks = db.query(Risk).all()
    resources = db.query(Resource).all()
    scenarios = db.query(Scenario).all()
    reports = db.query(Report).all()

    estimates_with_actuals = [
        estimate for estimate in estimates
        if estimate.actual_effort_hours and estimate.actual_effort_hours > 0
    ]
    effort_errors = [
        abs(estimate.estimated_effort_hours - estimate.actual_effort_hours) / estimate.actual_effort_hours * 100
        for estimate in estimates_with_actuals
    ]
    average_accuracy = 100 - min(sum(effort_errors) / len(effort_errors), 100) if effort_errors else None

    status_counter = Counter(project.status.value if hasattr(project.status, "value") else str(project.status) for project in projects)
    domain_counter = Counter((project.department or "General") for project in projects)
    risk_distribution = Counter(risk.category for risk in risks)
    risk_exposure_by_project = defaultdict(float)
    for risk in risks:
        risk_exposure_by_project[risk.project_id] += (_safe(risk.probability) * _safe(risk.impact))

    method_summary = defaultdict(lambda: {"count": 0, "total_effort": 0.0, "total_cost": 0.0, "confidence": 0.0})
    for estimate in estimates:
        summary = method_summary[estimate.estimation_method]
        summary["count"] += 1
        summary["total_effort"] += _safe(estimate.estimated_effort_hours)
        summary["total_cost"] += _safe(estimate.estimated_cost)
        summary["confidence"] += _safe(estimate.confidence_level)

    productivity_by_domain = defaultdict(list)
    for project in historical_projects:
        if project.productivity:
            productivity_by_domain[project.domain or project.industry or "General"].append(project.productivity)

    historical_accuracy = []
    for project in historical_projects:
        if project.estimated_effort_hours and project.actual_effort_hours:
            error = abs(project.estimated_effort_hours - project.actual_effort_hours) / project.actual_effort_hours * 100
            historical_accuracy.append({
                "project": project.project_name,
                "domain": project.domain or project.industry,
                "estimated_effort": round(project.estimated_effort_hours, 2),
                "actual_effort": round(project.actual_effort_hours, 2),
                "accuracy": round(100 - min(error, 100), 2),
            })

    project_health = []
    for project in projects:
        project_estimates = [estimate for estimate in estimates if estimate.project_id == project.id]
        project_resources = [resource for resource in resources if resource.project_id == project.id]
        latest_estimate = project_estimates[-1] if project_estimates else None
        budget = _safe(project.budget)
        forecast_cost = _safe(latest_estimate.estimated_cost if latest_estimate else None)
        budget_pressure = forecast_cost / budget if budget else 0
        exposure = risk_exposure_by_project.get(project.id, 0)
        allocation = sum(_safe(resource.allocation_percentage) for resource in project_resources)
        health_score = max(0, min(100, 100 - exposure * 35 - max(0, budget_pressure - 1) * 30 - max(0, allocation - 100) * 0.2))
        project_health.append({
            "project_id": project.id,
            "name": project.name,
            "status": project.status.value if hasattr(project.status, "value") else str(project.status),
            "budget": budget,
            "forecast_cost": forecast_cost,
            "risk_exposure": round(exposure, 3),
            "resource_allocation": round(allocation, 2),
            "health_score": round(health_score, 1),
        })

    return {
        "portfolio": {
            "projects": len(projects),
            "active_projects": sum(1 for project in projects if str(project.status.value if hasattr(project.status, "value") else project.status) in {"planning", "in_progress", "on_hold"}),
            "historical_records": len(historical_projects),
            "estimates": len(estimates),
            "risks": len(risks),
            "scenarios": len(scenarios),
            "resources": len(resources),
            "reports": len(reports),
            "portfolio_budget": round(sum(_safe(project.budget) for project in projects), 2),
            "average_estimation_accuracy": round(average_accuracy, 2) if average_accuracy is not None else None,
        },
        "project_status_trend": [{"label": label, "value": value} for label, value in status_counter.items()],
        "domain_distribution": [{"label": label, "value": value} for label, value in domain_counter.items()],
        "estimation_comparison": [
            {
                "method": method,
                "count": values["count"],
                "average_effort": round(values["total_effort"] / values["count"], 2),
                "average_cost": round(values["total_cost"] / values["count"], 2),
                "average_confidence": round(values["confidence"] / values["count"], 2),
            }
            for method, values in method_summary.items()
        ],
        "risk_analysis": {
            "distribution": [{"label": label, "value": value} for label, value in risk_distribution.items()],
            "total_exposure": round(sum((_safe(risk.probability) * _safe(risk.impact)) for risk in risks), 3),
            "high_risk_count": sum(1 for risk in risks if (_safe(risk.probability) * _safe(risk.impact)) >= 0.35),
        },
        "productivity_metrics": [
            {"domain": domain, "average_productivity": round(sum(values) / len(values), 2), "records": len(values)}
            for domain, values in productivity_by_domain.items()
        ],
        "historical_accuracy": sorted(historical_accuracy, key=lambda item: item["accuracy"])[:15],
        "project_health": sorted(project_health, key=lambda item: item["health_score"]),
        "ml_summary": build_ml_insights(historical_projects),
    }
