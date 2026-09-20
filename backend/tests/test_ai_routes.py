import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import AIConversation, AIMessage
from app.modules.ai.repositories.conversation import ConversationRepository, MessageRepository
from app.modules.ai.services.conversation import ConversationService
from app.modules.ai.services.langgraph_service import LangGraphAIService
from app.modules.ai.tools import create_tool_registry
from app.modules.ai.memory.session_memory import SessionMemory
from app.modules.ai.schemas.ai import ChatRequest


@pytest.mark.asyncio
async def test_create_conversation(db_session: AsyncSession):
    service = ConversationService(db_session)
    conversation = await service.create_conversation(
        session_id="test-session-1",
        agent_type="router",
        is_active=True,
    )
    assert conversation.id is not None
    assert conversation.session_id == "test-session-1"


@pytest.mark.asyncio
async def test_get_or_create_active(db_session: AsyncSession):
    service = ConversationService(db_session)
    conversation = await service.get_or_create_active("test-session-2", uuid.uuid4())
    assert conversation.is_active is True

    same = await service.get_or_create_active("test-session-2", uuid.uuid4())
    assert same.id == conversation.id


@pytest.mark.asyncio
async def test_add_message(db_session: AsyncSession):
    service = ConversationService(db_session)
    conversation = await service.create_conversation(
        session_id="test-session-3",
        agent_type="router",
        is_active=True,
    )
    message = await service.add_message(
        conversation_id=conversation.id,
        role="user",
        content="Hello",
    )
    assert message.id is not None
    assert message.content == "Hello"


@pytest.mark.asyncio
async def test_conversation_repository_get_by_session_id(db_session: AsyncSession):
    repo = ConversationRepository(db_session)
    service = ConversationService(db_session)
    await service.create_conversation(
        session_id="test-session-4",
        agent_type="router",
        is_active=True,
    )
    found = await repo.get_by_session_id("test-session-4")
    assert found is not None
    assert found.session_id == "test-session-4"


@pytest.mark.asyncio
async def test_message_repository_list_by_conversation(db_session: AsyncSession):
    repo = MessageRepository(db_session)
    service = ConversationService(db_session)
    conversation = await service.create_conversation(
        session_id="test-session-5",
        agent_type="router",
        is_active=True,
    )
    await service.add_message(conversation_id=conversation.id, role="user", content="Hi")
    await service.add_message(conversation_id=conversation.id, role="assistant", content="Hello")
    messages = await repo.list_by_conversation(conversation.id)
    assert len(messages) == 2


@pytest.mark.asyncio
async def test_session_memory_operations():
    memory = SessionMemory()
    session_id = "test-memory-session"
    memory.append_message(session_id, "user", "Hello")
    memory.append_message(session_id, "assistant", "Hi there")
    session = memory.get(session_id)
    assert session is not None
    assert len(session["history"]) == 2
    memory.clear(session_id)
    assert memory.get(session_id) is None


@pytest.mark.asyncio
async def test_langgraph_chat():
    tool_registry = create_tool_registry()
    service = LangGraphAIService(tool_registry)
    request = ChatRequest(message="What products do you have?", session_id="test-session-6")
    response = await service.chat(request)
    assert response.session_id == "test-session-6"
    assert response.message is not None
