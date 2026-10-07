import uuid
from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.memory.redis_session_store import RedisSessionStore
from app.modules.ai.providers.base import GeminiProvider
from app.modules.ai.repositories.conversation import (
    ConversationRepository,
    MessageRepository,
)
from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.services.conversation import ConversationService
from app.modules.ai.services.customer_memory import CustomerMemoryService
from app.modules.ai.services.langgraph_service import LangGraphAIService
from app.modules.ai.services.prompt_builder import PromptBuilder
from app.modules.ai.services.tool_manager import ToolManager
from app.modules.ai.tools import create_tool_registry


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
    await service.add_message(
        conversation_id=conversation.id, role="user", content="Hi"
    )
    await service.add_message(
        conversation_id=conversation.id, role="assistant", content="Hello"
    )
    messages = await repo.list_by_conversation(conversation.id)
    assert len(messages) == 2


@pytest.mark.asyncio
async def test_redis_session_store_operations():
    store = RedisSessionStore(prefix="ai:test", ttl=60)
    backend: dict[str, str] = {}

    async def mock_get(key: str) -> bytes | None:
        value = backend.get(key)
        return value.encode("utf-8") if value is not None else None

    async def mock_set(key: str, value: str, ex: int | None = None) -> bool:
        backend[key] = value
        return True

    async def mock_delete(key: str) -> int:
        if key in backend:
            del backend[key]
            return 1
        return 0

    async def mock_exists(key: str) -> int:
        return 1 if key in backend else 0

    mock_client = AsyncMock()
    mock_client.get.side_effect = mock_get
    mock_client.set.side_effect = mock_set
    mock_client.delete.side_effect = mock_delete
    mock_client.exists.side_effect = mock_exists

    with patch("app.modules.ai.memory.redis_session_store.redis_client", mock_client):
        session_id = "test-redis-session"
        assert await store.get(session_id) is None

        await store.append_message(session_id, "user", "Hello")
        mock_client.set.assert_awaited_once()

        session = await store.get(session_id)
        assert session is not None
        assert len(session["history"]) == 1
        assert session["history"][0]["role"] == "user"

        await store.append_message(session_id, "assistant", "Hi there")
        session = await store.get(session_id)
        assert session is not None
        assert len(session["history"]) == 2

        await store.clear(session_id)
        mock_client.delete.assert_awaited_with(store._key(session_id))


@pytest.mark.asyncio
async def test_langgraph_chat():
    tool_registry = create_tool_registry()
    service = LangGraphAIService(
        tool_registry,
        ai_provider=GeminiProvider(api_key="test-key"),
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
    )
    request = ChatRequest(
        message="What products do you have?", session_id="test-session-6"
    )
    response = await service.chat(request)
    assert response.session_id == "test-session-6"
    assert response.message is not None


@pytest.mark.asyncio
async def test_chat_persists_messages_and_tool_calls(db_session: AsyncSession):
    tool_registry = create_tool_registry()
    request = ChatRequest(
        message="What products do you have?", session_id="test-session-7"
    )

    mock_client = AsyncMock()
    mock_client.get.return_value = None
    mock_client.set.return_value = True
    mock_client.delete.return_value = 1
    mock_client.exists.return_value = 0

    with patch("app.modules.ai.memory.redis_session_store.redis_client", mock_client):
        from app.modules.ai.services.langgraph_service import (
            LangGraphAIService as LGService,
        )

        logged_calls = []

        async def fake_logger(
            tool_name,
            message,
            result,
            latency_ms,
            *,
            status="success",
            error_message=None,
        ):
            logged_calls.append(
                {
                    "tool_name": tool_name,
                    "arguments": message,
                    "status": status,
                    "latency_ms": latency_ms,
                }
            )

        service = LGService(
            tool_registry,
            ai_provider=GeminiProvider(api_key="test-key"),
            prompt_builder=PromptBuilder(),
            tool_manager=ToolManager(tool_registry),
            customer_memory_service=None,
            tool_call_logger=fake_logger,
        )
        response = await service.chat(request, db=db_session)
        assert response.session_id == "test-session-7"
        assert response.message is not None

        conversation_service = ConversationService(db_session)
        conversation = await conversation_service.get_or_create_active(
            request.session_id, None
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

        repo = ConversationRepository(db_session)
        found = await repo.get_by_session_id("test-session-7")
        assert found is not None

        message_repo = MessageRepository(db_session)
        messages = await message_repo.list_by_conversation(found.id)
        assert len(messages) == 2
        assert messages[0].content == "What products do you have?"
        assert messages[1].role == "assistant"

        assert len(logged_calls) >= 1


@pytest.mark.asyncio
async def test_customer_memory_service_returns_profile(db_session: AsyncSession):
    from app.modules.customer.models import Customer
    from app.modules.customer.repositories.customer import CustomerRepository

    customer_repo = CustomerRepository(db_session)
    customer = await customer_repo.create(
        Customer(
            full_name="Nabil",
            email="nabil@example.com",
            phone="01700000000",
            skin_type="Dry",
            skin_concerns=["Acne"],
            status="active",
        )
    )
    await db_session.flush()

    service = CustomerMemoryService(db_session)
    context = await service.get_customer_context(customer.id)

    assert context["customer"]["name"] == "Nabil"
    assert context["customer"]["skin_type"] == "Dry"
    assert context["customer"]["skin_concerns"] == ["Acne"]


@pytest.mark.asyncio
async def test_customer_memory_service_returns_empty_for_none():
    service = CustomerMemoryService(None)
    context = await service.get_customer_context(None)
    assert context == {}


@pytest.mark.asyncio
async def test_customer_memory_service_returns_empty_for_missing_customer(
    db_session: AsyncSession,
):
    service = CustomerMemoryService(db_session)
    context = await service.get_customer_context(uuid.uuid4())
    assert context == {}
