import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import ActivityLog
from app.modules.admin.repositories.activity_log import ActivityLogRepository


class ActivityLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ActivityLogRepository(session)

    async def create(self, **kwargs: Any) -> ActivityLog:
        log = ActivityLog(**kwargs)
        return await self.repository.create(log)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        user_id: uuid.UUID | None = None,
        action: str | None = None,
    ) -> tuple[list[ActivityLog], int]:
        filters: dict[str, Any] = {}
        if user_id is not None:
            filters["user_id"] = user_id
        if action is not None:
            filters["action"] = action
        return await self.repository.get_list(skip=skip, limit=limit, **filters)
