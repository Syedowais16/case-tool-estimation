"""Notification endpoints for reminders, deadlines, risk alerts, and reviews."""
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config.settings import get_settings
from app.core.security.security import get_current_user
from app.db.base import get_db
from app.models.project_models import Project
from app.models.report_models import Notification
from app.models.scenario_models import Risk
from app.models.user_models import User

router = APIRouter(prefix="/notifications", tags=["notifications"])
settings = get_settings()


def _serialize(notification: Notification) -> dict:
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "project_id": notification.project_id,
        "title": notification.title,
        "message": notification.message,
        "notification_type": notification.notification_type,
        "severity": notification.severity,
        "channel": notification.channel,
        "is_read": notification.is_read,
        "due_at": notification.due_at,
        "sent_at": notification.sent_at,
        "metadata": notification.event_metadata,
        "created_at": notification.created_at,
    }


def _email_configured() -> bool:
    return all([settings.smtp_server, settings.smtp_port, settings.smtp_username, settings.smtp_password, settings.smtp_from_email])


def _send_email(to_email: str, subject: str, body: str) -> bool:
    if not _email_configured():
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_from_email
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)
    return True


def _create_if_missing(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str,
    severity: str = "info",
    project_id: int | None = None,
    due_at: datetime | None = None,
    metadata: dict | None = None,
) -> Notification | None:
    existing = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.title == title,
        Notification.project_id == project_id,
        Notification.is_read == False,
    ).first()
    if existing:
        return None
    notification = Notification(
        user_id=user_id,
        project_id=project_id,
        title=title,
        message=message,
        notification_type=notification_type,
        severity=severity,
        channel="in_app",
        due_at=due_at,
        event_metadata=metadata or {},
    )
    db.add(notification)
    return notification


@router.get("")
async def list_notifications(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List notifications for the signed-in user."""
    query = db.query(Notification).filter(Notification.user_id == int(current_user["user_id"]))
    if unread_only:
        query = query.filter(Notification.is_read == False)
    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    return {
        "total": query.count(),
        "unread": query.filter(Notification.is_read == False).count() if not unread_only else len(notifications),
        "data": [_serialize(notification) for notification in notifications],
    }


@router.post("/refresh")
async def refresh_notifications(
    send_email: bool = False,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Generate alerts from live projects, deadlines, risks, and estimate reviews."""
    user_id = int(current_user["user_id"])
    user = db.query(User).filter(User.id == user_id).first()
    now = datetime.utcnow()
    created = []

    projects = db.query(Project).filter(Project.is_active == True).all()
    for project in projects:
        if project.end_date and now <= project.end_date <= now + timedelta(days=14):
            created.append(_create_if_missing(
                db,
                user_id=user_id,
                project_id=project.id,
                title=f"Deadline approaching: {project.name}",
                message=f"{project.name} is due on {project.end_date.date()}. Review remaining estimates, risks, and staffing.",
                notification_type="deadline",
                severity="warning",
                due_at=project.end_date,
                metadata={"project_name": project.name},
            ))

    risks = db.query(Risk).filter(Risk.status == "active").all()
    for risk in risks:
        exposure = (risk.probability or 0) * (risk.impact or 0)
        if exposure >= 0.35:
            created.append(_create_if_missing(
                db,
                user_id=user_id,
                project_id=risk.project_id,
                title=f"High risk exposure: {risk.category}",
                message=f"{risk.description} has exposure score {round(exposure, 2)}. Mitigation: {risk.mitigation_strategy or 'Add mitigation plan.'}",
                notification_type="risk",
                severity="critical" if exposure >= 0.55 else "warning",
                metadata={"risk_id": risk.id, "exposure": round(exposure, 3)},
            ))

    created = [notification for notification in created if notification is not None]
    db.commit()

    emailed = 0
    if send_email and user:
        for notification in created:
            if _send_email(user.email, notification.title, notification.message):
                notification.channel = "email"
                notification.sent_at = datetime.utcnow()
                emailed += 1
        db.commit()

    return {
        "created": len(created),
        "email_configured": _email_configured(),
        "emails_sent": emailed,
        "data": [_serialize(notification) for notification in created],
    }


@router.put("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Mark one notification as read."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == int(current_user["user_id"]),
    ).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    notification.is_read = True
    db.commit()
    return _serialize(notification)


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete one notification."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == int(current_user["user_id"]),
    ).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
