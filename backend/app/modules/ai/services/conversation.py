import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import AIConversation, AIMessage
from app.modules.ai.repositories.conversation import (
    ConversationRepository,
    MessageRepository,
)
from app.modules.ai.repositories.session_state import SessionStateRepository


class ConversationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ConversationRepository(session)
        self.message_repository = MessageRepository(session)
        self.session_state_repository = SessionStateRepository(session)

    async def create_conversation(self, **kwargs: Any) -> AIConversation:
        conversation = AIConversation(**kwargs)
        return await self.repository.create(conversation)

    async def get_or_create_active(
        self, session_id: str, user_id: uuid.UUID | None
    ) -> AIConversation:
        conversation = await self.repository.get_by_session_id(session_id)
        if conversation and conversation.is_active:
            return conversation
        if conversation:
            conversation.is_active = False
            await self.repository.update(conversation, is_active=False)
        return await self.create_conversation(
            user_id=user_id,
            session_id=session_id,
            agent_type="router",
            is_active=True,
        )

    async def add_message(self, conversation_id: uuid.UUID, **kwargs: Any) -> AIMessage:
        message = AIMessage(conversation_id=conversation_id, **kwargs)
        return await self.message_repository.create(message)

    async def get_conversation_history(
        self, conversation_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> list[AIMessage]:
        return await self.message_repository.list_by_conversation(
            conversation_id, skip=skip, limit=limit
        )

    async def get_or_create_session_state(
        self, session_id: str, user_id: uuid.UUID | None
    ) -> Any:
        state = await self.session_state_repository.get_by_session_id(session_id)
        if not state:
            state = await self.session_state_repository.create(
                session_id=session_id,
                user_id=user_id,
                current_agent="router",
                intent=None,
                context=None,
                is_active=True,
            )
        return state
