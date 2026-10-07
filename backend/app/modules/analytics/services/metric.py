from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import Metric
from app.modules.analytics.repositories.metric import MetricRepository


class MetricService:
    def __init__(self, session: AsyncSession):
        self.repository = MetricRepository(session)

    async def create(
        self,
        metric_name: str,
        metric_value: float,
        metric_type: str,
        dimensions: str | None = None,
        recorded_at: str | None = None,
    ) -> Any:
        if recorded_at is None:
            recorded_at = datetime.now(UTC).isoformat()

        metric = Metric(
            metric_name=metric_name,
            metric_value=metric_value,
            metric_type=metric_type,
            dimensions=dimensions,
            recorded_at=recorded_at,
        )
        return await self.repository.create(metric)

    async def get_by_name(self, name: str, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_by_name(name, skip=skip, limit=limit)
