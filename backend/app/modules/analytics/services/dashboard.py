import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.models import Dashboard
from app.modules.analytics.repositories.dashboard import DashboardRepository
from typing import Any



class DashboardService:
    def __init__(self, session: AsyncSession):
        self.repository = DashboardRepository(session)

    async def create(
        self,
        name: str,
        description: str | None = None,
        is_public: bool = False,
        layout: str | None = None,
    ) -> Any:
        dashboard = Dashboard(
            name=name,
            description=description,
            is_public=is_public,
            layout=layout,
        )
        return await self.repository.create(dashboard)

    async def get_public(self, skip: int = 0, limit: int = 20) -> Any:
        return await self.repository.get_public(skip=skip, limit=limit)

    async def get_by_id(self, dashboard_id: uuid.UUID) -> Any:
        return await self.repository.get_by_id(dashboard_id)
