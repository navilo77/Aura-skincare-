from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import Dashboard
from app.modules.analytics.repositories.base import BaseRepository


class DashboardRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Dashboard)

    async def get_public(self, skip: int = 0, limit: int = 20) -> tuple[list[Any], int]:
        query = (
            select(Dashboard)
            .where(Dashboard.is_public == True)  # noqa: E712
            .order_by(Dashboard.created_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total
