from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.services.customer_memory import CustomerMemoryService
from app.modules.ai.services.langgraph_service import LangGraphAIService
from app.modules.ai.services.prompt_builder import PromptBuilder
from app.modules.ai.services.rag.rag_service import RAGService
from app.modules.ai.services.rag.schemas import (
    RetrievalContext,
    SearchQuery,
    SearchResult,
)
from app.modules.ai.services.tool_manager import ToolManager
from app.modules.ai.tools import create_tool_registry
from app.modules.knowledge.schemas.knowledge import ChunkMetadata

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_rag_called_for_knowledge_question(db_session: AsyncSession):
    """RAG must be invoked when the user asks about business knowledge (policy, shipping, returns, coupons)."""
    tool_registry = create_tool_registry()
    mock_rag_service = AsyncMock(spec=RAGService)
    mock_rag_service.search = AsyncMock(return_value=RetrievalContext(
        query="return policy",
        chunks=[
            SearchResult(
                chunk_id="c1",
                document_id="doc-return-001",
                content="Returns are accepted within 30 days of purchase.",
                similarity=0.89,
                category="Policy",
                metadata=ChunkMetadata(
                    document_id="doc-return-001",
                    chunk_id="c1",
                    category="Policy",
                    language="en",
                    version="1.0",
                    source="Operations",
                    created_at="2026-09-30",
                    updated_at="2026-09-30",
                ),
            )
        ],
        total_chunks=1,
        has_results=True,
    ))

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="Verified answer about returns.")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=mock_rag_service,
    )

    request = ChatRequest(message="What is your return policy?", session_id="t-rag-policy")
    response = await service.chat(request, db=db_session)

    mock_rag_service.search.assert_called_once()
    called_query = mock_rag_service.search.call_args[0][0]
    assert isinstance(called_query, SearchQuery)
    assert "return policy" in called_query.query
    assert called_query.status == "available"
    assert response.message is not None


@pytest.mark.asyncio
async def test_rag_called_for_shipping_question(db_session: AsyncSession):
    """RAG must be invoked for shipping / delivery knowledge questions."""
    tool_registry = create_tool_registry()
    mock_rag_service = AsyncMock(spec=RAGService)
    mock_rag_service.search = AsyncMock(return_value=RetrievalContext(
        query="shipping cost",
        chunks=[],
        total_chunks=0,
        has_results=False,
    ))

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="shipping answer")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=mock_rag_service,
    )

    request = ChatRequest(message="How much is delivery cost to Dhaka?", session_id="t-rag-shipping")
    await service.chat(request, db=db_session)

    mock_rag_service.search.assert_called_once()


@pytest.mark.asyncio
async def test_rag_not_called_for_product_search(db_session: AsyncSession):
    """RAG must NOT be called for pure product catalog questions (product tools handle those)."""
    tool_registry = create_tool_registry()
    mock_rag_service = AsyncMock(spec=RAGService)

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="product answer")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=mock_rag_service,
    )

    request = ChatRequest(message="Do you have any face cream?", session_id="t-rag-product")
    await service.chat(request, db=db_session)

    mock_rag_service.search.assert_not_called()


@pytest.mark.asyncio
async def test_rag_not_called_for_greeting(db_session: AsyncSession):
    """RAG must NOT be called for simple greetings."""
    tool_registry = create_tool_registry()
    mock_rag_service = AsyncMock(spec=RAGService)

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="hello answer")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=mock_rag_service,
    )

    request = ChatRequest(message="Hi, how are you?", session_id="t-rag-greet")
    await service.chat(request, db=db_session)

    mock_rag_service.search.assert_not_called()


@pytest.mark.asyncio
async def test_rag_context_reaches_prompt_builder():
    """Retrieved RAG context must be included in the built prompt (verified in build)."""
    prompt_builder = PromptBuilder()
    rag_context = RetrievalContext(
        query="return policy",
        chunks=[
            SearchResult(
                chunk_id="c1",
                document_id="doc-return-001",
                content="Returns are accepted within 30 days of purchase.",
                similarity=0.89,
                category="Policy",
                metadata=ChunkMetadata(
                    document_id="doc-return-001",
                    chunk_id="c1",
                    category="Policy",
                    language="en",
                    version="1.0",
                    source="Operations",
                    created_at="2026-09-30",
                    updated_at="2026-09-30",
                ),
            )
        ],
        total_chunks=1,
        has_results=True,
    )

    prompt = prompt_builder.build({
        "request": ChatRequest(message="What is your return policy?", session_id="t-pb"),
        "history": [],
        "tool_results": None,
        "customer_context": None,
        "rag_context": rag_context,
    })

    assert "Aura Business Knowledge (verified):" in prompt
    assert "[Policy]" in prompt
    assert "Returns are accepted within 30 days of purchase." in prompt


@pytest.mark.asyncio
async def test_rag_context_not_added_when_empty():
    """No RAG section should appear when there are no retrieved chunks."""
    prompt_builder = PromptBuilder()
    rag_context = RetrievalContext(
        query="unknown term",
        chunks=[],
        total_chunks=0,
        has_results=False,
    )

    prompt = prompt_builder.build({
        "request": ChatRequest(message="unknown term?", session_id="t-pb2"),
        "history": [],
        "tool_results": None,
        "customer_context": None,
        "rag_context": rag_context,
    })

    assert "Aura Business Knowledge (verified):" not in prompt


@pytest.mark.asyncio
async def test_product_search_still_works_without_rag(db_session: AsyncSession):
    """Product tool search must still work when rag_service is not wired (None)."""
    tool_registry = create_tool_registry()

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="No products found in catalog right now.")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=None,
    )

    request = ChatRequest(message="What products do you have?", session_id="t-product-no-rag")
    response = await service.chat(request, db=db_session)

    assert response.session_id == "t-product-no-rag"
    assert response.message is not None
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].get("tool") == "search_products"
    assert response.tool_calls[0].get("total") == 0


@pytest.mark.asyncio
async def test_rag_graceful_failure_returns_empty_context(db_session: AsyncSession):
    """If RAG retrieval fails (e.g. embedding unavailable), the flow must not crash."""
    tool_registry = create_tool_registry()
    mock_rag_service = AsyncMock(spec=RAGService)
    mock_rag_service.search = AsyncMock(side_effect=Exception("embedding service unavailable"))

    mock_ai_provider = AsyncMock()
    mock_ai_provider.generate = AsyncMock(return_value="fallback answer")

    service = LangGraphAIService(
        tool_registry,
        ai_provider=mock_ai_provider,
        prompt_builder=PromptBuilder(),
        tool_manager=ToolManager(tool_registry),
        customer_memory_service=None,
        rag_service=mock_rag_service,
    )

    request = ChatRequest(message="What is your return policy?", session_id="t-rag-error")
    response = await service.chat(request, db=db_session)

    assert response.session_id == "t-rag-error"
    assert response.message is not None


@pytest.mark.asyncio
async def test_no_direct_db_access_from_agent():
    """CustomerAIAgent must access business knowledge only through RAGService, never VectorStore/DB directly."""
    import ast
    import inspect

    from app.modules.ai.agents.customer_agent import CustomerAIAgent

    source = inspect.getsource(CustomerAIAgent)
    tree = ast.parse(source)

    direct_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if any(
                k in module
                for k in ("vector_store", "knowledge_chunk", "embedding_service", "retriever")
            ):
                direct_imports.append(module)

    assert not direct_imports, f"Agent must not import DB/vector layers directly: {direct_imports}"

    # Also confirm RAGService is used only via the injected rag_service attribute.
    assert "self.rag_service.search" in source
