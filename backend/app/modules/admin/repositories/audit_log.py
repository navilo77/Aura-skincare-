import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import AuditLog
from app.modules.admin.repositories.base import BaseRepository


class AuditLogRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AuditLog)

    async def list_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[AuditLog]:
        return await self.get_list(skip=skip, limit=limit, user_id=user_id)

    async def list_by_entity(
        self, entity_type: str, entity_id: uuid.UUID | None = None
    ) -> list[AuditLog]:
        filters = {"entity_type": entity_type}
        if entity_id is not None:
            filters["entity_id"] = entity_id
        return await self.get_list_by_filters(filters)
