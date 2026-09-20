import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import AIConversation, AIMessage
from app.modules.ai.repositories.base import BaseRepository


class ConversationRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIConversation)

    async def get_by_session_id(self, session_id: str) -> AIConversation | None:
        return await self.get_by_field("session_id", session_id)

    async def list_by_user(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> list[AIConversation]:
        result, _ = await self.get_list(skip=skip, limit=limit, user_id=user_id)
        return result


class MessageRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIMessage)

    async def list_by_conversation(
        self, conversation_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> list[AIMessage]:
        result, _ = await self.get_list(
            skip=skip, limit=limit, conversation_id=conversation_id
        )
        return result
