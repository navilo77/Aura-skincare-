import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import SessionState
from app.modules.ai.repositories.base import BaseRepository


class SessionStateRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, SessionState)

    async def get_by_session_id(self, session_id: str) -> SessionState | None:
        return await self.get_by_field("session_id", session_id)

    async def list_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[SessionState]:
        result, _ = await self.get_list(skip=skip, limit=limit, user_id=user_id)
        return result
