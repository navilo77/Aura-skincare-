from typing import Any


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import Metric
from app.modules.analytics.repositories.base import BaseRepository


class MetricRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Metric)

    async def get_by_name(self, name: str, skip: int = 0, limit: int = 20) -> tuple[list[Any], int]:
        query = (
            select(Metric)
            .where(Metric.metric_name == name)
            .order_by(Metric.recorded_at.desc())
        )
        paginated, total = await self._apply_pagination(query, skip, limit)
        result = await self.session.execute(paginated)
        return list(result.scalars().all()), total
