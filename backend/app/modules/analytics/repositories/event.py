import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import AnalyticsEvent
from app.modules.analytics.repositories.base import BaseRepository


class AnalyticsEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, AnalyticsEvent)

    async def get_by_category(
        self, category: str, skip: int = 0, limit: int = 20
    ) -> tuple[list[Any], int]:
        query = (
            select(AnalyticsEvent)
            .where(AnalyticsEvent.event_category == category)
            .order_by(AnalyticsEvent.created_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total

    async def get_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Any], int]:
        query = (
            select(AnalyticsEvent)
            .where(AnalyticsEvent.user_id == user_id)
            .order_by(AnalyticsEvent.created_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total
