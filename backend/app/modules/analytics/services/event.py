import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import AnalyticsEvent
from app.modules.analytics.repositories.event import AnalyticsEventRepository
from typing import Any



class EventService:
    def __init__(self, session: AsyncSession):
        self.repository = AnalyticsEventRepository(session)

    async def create(
        self,
        event_name: str,
        event_category: str,
        properties: str | None = None,
        user_id: uuid.UUID | None = None,
        session_id: str | None = None,
    ) -> Any:
        event = AnalyticsEvent(
            event_name=event_name,
            event_category=event_category,
            properties=properties,
            user_id=user_id,
            session_id=session_id,
        )
        return await self.repository.create(event)

    async def get_by_category(self, category: str, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_by_category(category, skip=skip, limit=limit)

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_by_user(user_id, skip=skip, limit=limit)
