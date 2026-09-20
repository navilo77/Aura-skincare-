import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import ActivityLog
from app.modules.admin.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ActivityLog)

    async def list_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[ActivityLog]:
        return await self.get_list(skip=skip, limit=limit, user_id=user_id)
