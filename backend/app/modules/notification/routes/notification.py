import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notification.models import Notification, NotificationTemplate
from app.modules.notification.schemas.notification import (
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
    TemplateCreate,
    TemplateRead,
    TemplateUpdate,
)
from app.modules.notification.services.notification import NotificationService
from app.modules.notification.services.template import TemplateService
from app.shared.database.session import get_db
from app.modules.notification.models import Notification, NotificationTemplate

router = APIRouter(tags=["notifications"])


@router.get("/templates", response_model=list[TemplateRead])
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    channel: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = TemplateService(db)
    templates = await service.get_active(channel=channel)
    return templates


@router.post(
    "/templates", response_model=TemplateRead, status_code=status.HTTP_201_CREATED
)
async def create_template(payload: TemplateCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = TemplateService(db)
    try:
        template = await service.create(
            name=payload.name,
            subject=payload.subject,
            body=payload.body,
            channel=payload.channel,
            is_active=payload.is_active,
        )
        return template
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.patch(
    "/templates/{template_id}", response_model=TemplateRead
)
async def update_template(
    template_id: uuid.UUID,
    payload: TemplateUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = TemplateService(db)
    try:
        template = await service.update(
            template_id=template_id,
            name=payload.name,
            subject=payload.subject,
            body=payload.body,
            channel=payload.channel,
            is_active=payload.is_active,
        )
        return template
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.post("", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification(
    payload: NotificationCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = NotificationService(db)
    notification = await service.create(
        user_id=payload.user_id,
        subject=payload.subject,
        body=payload.body,
        channel=payload.channel,
        template_id=payload.template_id,
    )
    return notification


@router.patch(
    "/{notification_id}", response_model=NotificationRead
)
async def update_notification(
    notification_id: uuid.UUID,
    payload: NotificationUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = NotificationService(db)
    try:
        notification = await service.update_status(
            notification_id=notification_id,
            status=payload.status or "pending",
            error_message=payload.error_message,
            sent_at=payload.sent_at,
        )
        return notification
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("", response_model=list[NotificationRead])
async def list_notifications(
    user_id: uuid.UUID | None = Query(None),
    status: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = NotificationService(db)
    if user_id:
        notifications, _ = await service.get_by_user(
            user_id, skip=skip, limit=limit
        )
    elif status:
        notifications, _ = await service.get_by_status(status, skip=skip, limit=limit)
    else:
        notifications = []
    return notifications
