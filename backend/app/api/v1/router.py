"""API v1 Router"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    projects,
    estimates,
    scenario_risk_resource,
    reports,
    dashboard,
    notifications,
    integrations,
)

api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(projects.router)
api_router.include_router(estimates.router)
api_router.include_router(scenario_risk_resource.router)
api_router.include_router(reports.router)
api_router.include_router(dashboard.router)
api_router.include_router(notifications.router)
api_router.include_router(integrations.router)
