import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.admin.models import AuditLog
from app.modules.admin.repositories.audit_log import AuditLogRepository


class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AuditLogRepository(session)

    async def create(self, **kwargs: Any) -> AuditLog:
        log = AuditLog(**kwargs)
        return await self.repository.create(log)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        user_id: uuid.UUID | None = None,
        entity_type: str | None = None,
    ) -> tuple[list[AuditLog], int]:
        filters: dict[str, Any] = {}
        if user_id is not None:
            filters["user_id"] = user_id
        if entity_type is not None:
            filters["entity_type"] = entity_type
        return await self.repository.get_list(skip=skip, limit=limit, **filters)
