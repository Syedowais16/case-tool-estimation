"""Jira and Trello integration endpoints."""
from datetime import datetime
from typing import Any, Dict, List

import requests
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config.settings import get_settings
from app.core.security.security import get_current_user
from app.db.base import get_db
from app.models.estimation_models import Estimate
from app.models.project_models import Project, ProjectStatus, ProjectVersion
from app.models.report_models import IntegrationSync

router = APIRouter(prefix="/integrations", tags=["integrations"])
settings = get_settings()


def _ensure_response(response: requests.Response, provider: str) -> Dict[str, Any] | List[Dict[str, Any]]:
    if response.ok:
        return response.json()
    print("JIRA STATUS:", response.status_code)
    print("JIRA RESPONSE:", response.text)
    detail = response.text[:500] if response.text else response.reason
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail=f"{provider} API request failed with {response.status_code}: {detail}"
    )


def _get_or_create_project(
    db: Session,
    name: str,
    description: str,
    user_id: int,
    task_count: int,
    completed_count: int,
    external_url: str | None = None,
) -> Project:
    project = db.query(Project).filter(Project.name == name).first()
    progress = completed_count / task_count if task_count else 0
    if project:
        project.description = description
        project.status = ProjectStatus.COMPLETED if progress >= 1 else ProjectStatus.IN_PROGRESS if progress > 0 else ProjectStatus.PLANNING
        project.team_size = max(project.team_size or 0, min(12, max(2, round(task_count / 8) + 1)))
        project.updated_at = datetime.utcnow()
        db.flush()
        return project

    project = Project(
        name=name,
        description=description + (f"\nExternal URL: {external_url}" if external_url else ""),
        created_by=user_id,
        status=ProjectStatus.COMPLETED if progress >= 1 else ProjectStatus.IN_PROGRESS if progress > 0 else ProjectStatus.PLANNING,
        budget=max(15000.0, task_count * 1800.0),
        team_size=min(12, max(2, round(task_count / 8) + 1)),
        client_name="External integration",
        project_manager="Imported from integration",
        department="Integration",
    )
    db.add(project)
    db.flush()
    version = ProjectVersion(
        project_id=project.id,
        version_number=1,
        description="Imported external planning baseline.",
        scope=f"Imported {task_count} work items from Jira/Trello for estimation mapping and progress tracking.",
        assumptions="Each imported issue/card is mapped to planning work; detailed estimate should be reviewed by the project manager.",
        constraints="External data quality depends on board hygiene, status mapping, and available story point fields.",
    )
    db.add(version)
    db.flush()
    effort = max(80.0, task_count * 18.0)
    duration = max(1.0, effort / 152 / max(project.team_size or 2, 1))
    db.add(Estimate(
        project_id=project.id,
        version_id=version.id,
        created_by=user_id,
        estimation_method="External Task Mapping",
        estimated_effort_hours=round(effort, 2),
        estimated_duration_months=round(duration, 2),
        estimated_cost=round(effort * 62.5, 2),
        estimated_team_size=project.team_size,
        confidence_level=64,
        confidence_interval_low=round(effort * 0.78, 2),
        confidence_interval_high=round(effort * 1.28, 2),
        notes="Automatically generated from external task count. Review using COCOMO/FPA/Hybrid before final approval.",
        assumptions="Average imported task effort estimated at 18 hours unless detailed story points are available.",
    ))
    return project


@router.get("/status")
async def integration_status(current_user: dict = Depends(get_current_user)):
    """Return whether Jira and Trello credentials are configured."""
    return {
        "jira": {
            "configured": all([settings.jira_base_url, settings.jira_email, settings.jira_api_token]),
            "base_url": settings.jira_base_url,
            "project_key": settings.jira_project_key,
            "auth_method": "basic_email_api_token",
        },
        "trello": {
            "configured": all([settings.trello_api_key, settings.trello_api_token]),
            "board_id": settings.trello_board_id,
            "auth_method": "key_token",
        },
    }


@router.get("/syncs")
async def list_integration_syncs(
    provider: str | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List integration sync audit records."""
    query = db.query(IntegrationSync)
    if provider:
        query = query.filter(IntegrationSync.provider == provider)
    syncs = query.order_by(IntegrationSync.created_at.desc()).limit(50).all()
    return {
        "total": query.count(),
        "data": syncs,
    }


@router.post("/jira/sync")
async def sync_jira(
    jql: str | None = Query(default=None, description="Jira JQL query. Defaults to configured project key."),
    max_results: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Import Jira issues, map them to a local project, and track progress."""
    if not all([settings.jira_base_url, settings.jira_email, settings.jira_api_token]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Jira is not configured. Set JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN in backend/.env."
        )

    base_url = settings.jira_base_url.rstrip("/")
    query = jql or (f"project = {settings.jira_project_key} ORDER BY updated DESC" if settings.jira_project_key else "ORDER BY updated DESC")
    response = requests.get(
    f"{base_url}/rest/api/3/search/jql",
    params={
        "jql": query,
        "maxResults": max_results,
    },
    auth=(settings.jira_email, settings.jira_api_token),
    headers={
        "Accept": "application/json"
    },
    timeout=25,
)
    payload = _ensure_response(response, "Jira")
    issues = payload.get("issues", [])
    if not issues:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jira returned no visible issues for the query.")

    issue_fields = issues[0].get("fields", {})
    first_project = issue_fields.get("project", {})
    completed_count = sum( 1 for issue in issues if issue.get("fields", {}).get("status", {}).get("statusCategory", {}).get("key") == "done")
    project_name = f"[Jira] {first_project.get('name') or first_project.get('key')}"
    issue_summaries = []

    for issue in issues:
        fields = issue.get("fields", {})

    issue_summaries.append({
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "status": fields.get("status", {}).get("name"),
        "type": fields.get("issuetype", {}).get("name"),
        "url": f"{base_url}/browse/{issue.get('key')}",
    })
    progress = round(completed_count / len(issues) * 100, 2)
    description = (
        f"Imported from Jira project {first_project.get('key')}. "
        f"Tasks: {len(issues)}, completed: {completed_count}, progress: {progress}%.\n"
        "Use this mapping to compare task-based progress with CASE Tool estimates."
    )
    project = _get_or_create_project(
        db,
        name=project_name,
        description=description,
        user_id=int(current_user["user_id"]),
        task_count=len(issues),
        completed_count=completed_count,
        external_url=f"{base_url}/jira/software/projects/{first_project.get('key')}",
    )
    sync = IntegrationSync(
        provider="jira",
        external_id=first_project.get("key"),
        external_url=f"{base_url}/jira/software/projects/{first_project.get('key')}",
        mapped_project_id=project.id,
        status="completed",
        task_count=len(issues),
        completed_count=completed_count,
        progress_percentage=progress,
        payload={"jql": query, "issues": issue_summaries},
        imported_by=int(current_user["user_id"]),
    )
    db.add(sync)
    db.commit()
    db.refresh(sync)
    return {"message": "Jira sync completed", "project_id": project.id, "sync": sync, "issues": issue_summaries}


@router.post("/trello/sync")
async def sync_trello(
    board_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Import Trello cards/lists, map them to a local project, and track progress."""
    if not all([settings.trello_api_key, settings.trello_api_token]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trello is not configured. Set TRELLO_API_KEY and TRELLO_API_TOKEN in backend/.env."
        )
    selected_board_id = board_id or settings.trello_board_id
    if not selected_board_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provide board_id or set TRELLO_BOARD_ID in backend/.env.")

    auth_params = {"key": settings.trello_api_key, "token": settings.trello_api_token}
    board_response = requests.get(
        f"https://api.trello.com/1/boards/{selected_board_id}",
        params={**auth_params, "fields": "name,desc,url,dateLastActivity"},
        headers={"Accept": "application/json"},
        timeout=25,
    )
    board = _ensure_response(board_response, "Trello")
    cards_response = requests.get(
        f"https://api.trello.com/1/boards/{selected_board_id}/cards",
        params={**auth_params, "fields": "name,desc,closed,due,dateLastActivity,idList,url"},
        headers={"Accept": "application/json"},
        timeout=25,
    )
    cards = _ensure_response(cards_response, "Trello")
    lists_response = requests.get(
        f"https://api.trello.com/1/boards/{selected_board_id}/lists",
        params={**auth_params, "fields": "name,closed"},
        headers={"Accept": "application/json"},
        timeout=25,
    )
    lists = _ensure_response(lists_response, "Trello")
    list_names = {item["id"]: item["name"] for item in lists}
    completed_count = sum(
        1 for card in cards
        if card.get("closed") or any(keyword in list_names.get(card.get("idList"), "").lower() for keyword in ["done", "complete", "released", "closed"])
    )
    progress = round(completed_count / len(cards) * 100, 2) if cards else 0
    project_name = f"[Trello] {board.get('name')}"
    card_summaries = [
        {
            "name": card.get("name"),
            "list": list_names.get(card.get("idList"), "Unknown"),
            "due": card.get("due"),
            "closed": card.get("closed"),
            "url": card.get("url"),
        }
        for card in cards
    ]
    project = _get_or_create_project(
        db,
        name=project_name,
        description=(
            f"Imported from Trello board '{board.get('name')}'. "
            f"Cards: {len(cards)}, completed: {completed_count}, progress: {progress}%.\n"
            f"Board description: {board.get('desc') or 'No description'}"
        ),
        user_id=int(current_user["user_id"]),
        task_count=len(cards),
        completed_count=completed_count,
        external_url=board.get("url"),
    )
    sync = IntegrationSync(
        provider="trello",
        external_id=selected_board_id,
        external_url=board.get("url"),
        mapped_project_id=project.id,
        status="completed",
        task_count=len(cards),
        completed_count=completed_count,
        progress_percentage=progress,
        payload={"board": board, "lists": lists, "cards": card_summaries},
        imported_by=int(current_user["user_id"]),
    )
    db.add(sync)
    db.commit()
    db.refresh(sync)
    return {"message": "Trello sync completed", "project_id": project.id, "sync": sync, "cards": card_summaries}
