import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import SessionState
from app.modules.ai.repositories.session_state import SessionStateRepository


class SessionStateService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = SessionStateRepository(session)

    async def get_or_create(
        self,
        session_id: str,
        user_id: uuid.UUID | None,
    ) -> SessionState:
        state = await self.repository.get_by_session_id(session_id)
        if not state:
            state = await self.repository.create(
                SessionState(
                    session_id=session_id,
                    user_id=user_id,
                    current_agent="router",
                    intent=None,
                    context=None,
                    is_active=True,
                )
            )
        return state

    async def update_state(
        self,
        session_id: str,
        current_agent: str | None = None,
        intent: str | None = None,
        context: str | None = None,
    ) -> SessionState | None:
        state = await self.repository.get_by_session_id(session_id)
        if not state:
            return None

        if current_agent is not None:
            state.current_agent = current_agent
        if intent is not None:
            state.intent = intent
        if context is not None:
            state.context = context

        await self.repository.update(
            state,
            current_agent=state.current_agent,
            intent=state.intent,
            context=state.context,
        )
        return state
