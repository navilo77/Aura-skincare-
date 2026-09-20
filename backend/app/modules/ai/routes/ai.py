from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.ai.memory.session_memory import SessionMemory
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.conversation import ConversationService
from app.modules.ai.services.langgraph_service import LangGraphAIService
from app.modules.ai.tools import create_tool_registry
from app.shared.database.session import get_db

router = APIRouter(tags=["ai"])

tool_registry = create_tool_registry()
session_memory = SessionMemory()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> ChatResponse:
    user_id = current_user.id if current_user else None
    if not request.session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id is required",
        )

    history = session_memory.get(request.session_id)
    history_messages = history.get("history", []) if history else []

    langgraph_service = LangGraphAIService(tool_registry)
    response = await langgraph_service.chat(request, history=history_messages)

    session_memory.append_message(request.session_id, "user", request.message)
    session_memory.append_message(request.session_id, "assistant", response.message)

    conversation_service = ConversationService(db)
    await conversation_service.get_or_create_active(request.session_id, user_id)

    return response
