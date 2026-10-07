import uuid
from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.schemas.analytics import EventCreate, EventRead
from app.modules.analytics.services.event import EventService
from app.shared.database.session import get_db

router = APIRouter(tags=["analytics-events"])


@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, db: AsyncSession = Depends(get_db)) -> Any:
    service = EventService(db)
    event = await service.create(
        event_name=payload.event_name,
        event_category=payload.event_category,
        properties=payload.properties,
        user_id=payload.user_id,
        session_id=payload.session_id,
    )
    return event


@router.get("/events", response_model=list[EventRead])
async def list_events(
    category: str | None = Query(None),
    user_id: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = EventService(db)
    if category:
        events, _ = await service.get_by_category(category, skip=skip, limit=limit)
    elif user_id:
        events, _ = await service.get_by_user(
            uuid.UUID(user_id), skip=skip, limit=limit
        )
    else:
        events = []
    return events
