from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_optional_user
from app.config.settings import settings
from app.modules.ai.memory.redis_session_store import RedisSessionStore
from app.modules.ai.providers.base import GeminiProvider
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.conversation import ConversationService
from app.modules.ai.services.customer_memory import CustomerMemoryService
from app.modules.ai.services.langgraph_service import LangGraphAIService
from app.modules.ai.services.prompt_builder import PromptBuilder
from app.modules.ai.services.rag.embedding_service import EmbeddingService
from app.modules.ai.services.rag.rag_service import RAGService
from app.modules.ai.services.rag.vector_store import VectorStore
from app.modules.ai.services.session_state import SessionStateService
from app.modules.ai.services.tool_call_log import ToolCallLogService
from app.modules.ai.services.tool_manager import ToolManager
from app.modules.ai.tools import create_tool_registry
from app.shared.database.session import get_db

router = APIRouter(tags=["ai"])

tool_registry = create_tool_registry()
redis_session_store = RedisSessionStore()
gemini_provider = GeminiProvider(
    api_key=settings.gemini_api_key
    or settings.google_api_key
    or settings.ai_provider_api_key
)
prompt_builder = PromptBuilder()
tool_manager = ToolManager(tool_registry)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_optional_user),
) -> ChatResponse:
    user_id = current_user.id if current_user else None
    if not request.session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id is required",
        )

    history_data = await redis_session_store.get(request.session_id)
    history_messages = history_data.get("history", []) if history_data else []

    conversation_service = ConversationService(db)
    session_state_service = SessionStateService(db)
    tool_call_log_service = ToolCallLogService(db)
    customer_memory_service = CustomerMemoryService(db)
    rag_service = RAGService(
        embedding_service=EmbeddingService(),
        vector_store=VectorStore(db),
    )

    async def _tool_call_logger(
        tool_name: str,
        message: str,
        result: dict[str, Any],
        latency_ms: float,
        *,
        status: str = "success",
        error_message: str | None = None,
    ) -> None:
        await tool_call_log_service.log_tool_call(
            session_id=request.session_id,
            tool_name=tool_name,
            arguments=message,
            result=str(result),
            status=status,
            latency_ms=int(latency_ms),
            error_message=error_message,
        )

    langgraph_service = LangGraphAIService(
        tool_registry,
        ai_provider=gemini_provider,
        prompt_builder=prompt_builder,
        tool_manager=tool_manager,
        customer_memory_service=customer_memory_service,
        tool_call_logger=_tool_call_logger,
        rag_service=rag_service,
    )
    response = await langgraph_service.chat(
        request, history=history_messages, db=db, user_id=user_id
    )

    await redis_session_store.append_message(
        request.session_id, "user", request.message
    )
    await redis_session_store.append_message(
        request.session_id, "assistant", response.message
    )

    conversation = await conversation_service.get_or_create_active(
        request.session_id, user_id
    )
    await conversation_service.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
    )
    await conversation_service.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content=response.message,
    )

    await session_state_service.get_or_create(request.session_id, user_id)

    first_tool = None
    if response.tool_calls:
        first_tool = response.tool_calls[0].get("tool")
    await session_state_service.update_state(
        request.session_id,
        current_agent=response.agent_type,
        intent=first_tool,
        context=request.message[:255] if request.message else None,
    )

    return response
