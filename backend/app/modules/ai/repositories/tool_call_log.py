import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import ToolCallLog
from app.modules.ai.repositories.base import BaseRepository


class ToolCallLogRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ToolCallLog)

    async def list_by_session(
        self, session_id: str, skip: int = 0, limit: int = 20
    ) -> list[ToolCallLog]:
        result, _ = await self.get_list(skip=skip, limit=limit, session_id=session_id)
        return result

    async def list_by_message(self, message_id: uuid.UUID) -> list[ToolCallLog]:
        return await self.get_list_by_field("message_id", message_id)
