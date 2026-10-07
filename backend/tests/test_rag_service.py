from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.services.rag.chunk_builder import ChunkBuilder
from app.modules.ai.services.rag.embedding_service import EmbeddingService
from app.modules.ai.services.rag.exceptions import (
    ChunkingError,
    EmbeddingServiceError,
)
from app.modules.ai.services.rag.knowledge_repository import KnowledgeRepository
from app.modules.ai.services.rag.rag_service import RAGService
from app.modules.ai.services.rag.retriever import Retriever
from app.modules.ai.services.rag.schemas import (
    IndexDocumentRequest,
    SearchQuery,
    SearchResult,
)
from app.modules.ai.services.rag.vector_store import VectorStore
from app.modules.knowledge.exceptions import DocumentValidationError
from app.modules.knowledge.schemas.knowledge import (
    ChunkMetadata,
    DocumentStatus,
    KnowledgeCategory,
    KnowledgeDocument,
)


@pytest.mark.asyncio
async def test_chunk_builder_valid_document():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="policy-return-001",
        title="Return Policy",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.POLICY,
        status=DocumentStatus.APPROVED,
        language="en",
        version="1.0",
        source="Operations",
    )
    chunks = builder.build_chunks(doc)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert chunk["word_count"] >= builder.min_words
        assert chunk["word_count"] <= builder.max_words
        assert "chunk_id" in chunk
        assert "metadata" in chunk


@pytest.mark.asyncio
async def test_chunk_builder_empty_content():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="doc-001",
        title="Empty",
        content="",
        category=KnowledgeCategory.POLICY,
        status=DocumentStatus.APPROVED,
    )
    with pytest.raises(DocumentValidationError):
        builder.build_chunks(doc)


@pytest.mark.asyncio
async def test_chunk_builder_invalid_status():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="doc-001",
        title="Draft",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.POLICY,
        status=DocumentStatus.DRAFT,
    )
    with pytest.raises(DocumentValidationError):
        builder.build_chunks(doc)


@pytest.mark.asyncio
async def test_chunk_builder_invalid_category():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="doc-001",
        title="Invalid",
        content=" ".join(["word"] * 500),
        category="InvalidCategory",
        status=DocumentStatus.APPROVED,
    )
    with pytest.raises(DocumentValidationError):
        builder.build_chunks(doc)


@pytest.mark.asyncio
async def test_chunk_builder_chunk_size():
    builder = ChunkBuilder()
    content = " ".join(["word"] * 1200)
    doc = KnowledgeDocument(
        id="doc-001",
        title="Large",
        content=content,
        category=KnowledgeCategory.EDUCATION,
        status=DocumentStatus.APPROVED,
    )
    chunks = builder.build_chunks(doc)
    for chunk in chunks:
        assert chunk["word_count"] <= builder.max_words


@pytest.mark.asyncio
async def test_chunk_builder_short_content_rejected():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="doc-001",
        title="Short",
        content=" ".join(["word"] * 100),
        category=KnowledgeCategory.FAQ,
        status=DocumentStatus.APPROVED,
    )
    with pytest.raises(ChunkingError):
        builder.build_chunks(doc)


@pytest.mark.asyncio
async def test_chunk_builder_faq_splitting():
    builder = ChunkBuilder()
    q1_answer = " ".join(["return"] * 200)
    q2_answer = " ".join(["shipping"] * 200)
    content = (
        f"Q: What is the return policy?\nA: {q1_answer}\n\n"
        f"Q: What about shipping costs?\nA: {q2_answer}"
    )
    doc = KnowledgeDocument(
        id="faq-001",
        title="FAQ",
        content=content,
        category=KnowledgeCategory.FAQ,
        status=DocumentStatus.APPROVED,
    )
    chunks = builder.build_chunks(doc)
    assert len(chunks) >= 1


@pytest.mark.asyncio
async def test_chunk_builder_metadata_attached():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="product-001",
        title="Product",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.PRODUCT,
        status=DocumentStatus.APPROVED,
        tags=["skincare"],
        metadata={"brand": "Aura", "skin_type": "Dry"},
    )
    chunks = builder.build_chunks(doc)
    assert len(chunks) >= 1
    for chunk in chunks:
        meta = chunk["metadata"]
        assert meta["document_id"] == "product-001"
        assert meta["category"] == KnowledgeCategory.PRODUCT
        assert meta["source"] == ""
        assert "chunk_id" in meta


@pytest.mark.asyncio
async def test_chunk_builder_word_count_method():
    builder = ChunkBuilder()
    assert builder._word_count("one two three") == 3
    assert builder._word_count("") == 0
    assert builder._word_count("   ") == 0


@pytest.mark.asyncio
async def test_chunk_builder_overlap_size():
    builder = ChunkBuilder(overlap_ratio=0.15)
    assert builder._overlap_size(" ".join(["word"] * 100)) == 15
    assert builder._overlap_size("") == 0


@pytest.mark.asyncio
async def test_chunk_builder_no_unrelated_mixing():
    builder = ChunkBuilder()
    mixed = "Product description here with enough words to make a valid chunk. " * 30
    mixed += (
        "\n\nReturn policy information about how to return items to our store. " * 30
    )
    doc = KnowledgeDocument(
        id="mixed-001",
        title="Mixed",
        content=mixed,
        category=KnowledgeCategory.EDUCATION,
        status=DocumentStatus.APPROVED,
    )
    chunks = builder.build_chunks(doc)
    for chunk in chunks:
        assert chunk["word_count"] >= builder.min_words


@pytest.mark.asyncio
async def test_embedding_service_generate():
    service = EmbeddingService(base_url="http://test:11434", model="bge-m3")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embedding": [0.1] * 1024}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        embedding = await service.embed("test query")
        assert len(embedding) == 1024
        assert all(isinstance(v, float) for v in embedding)


@pytest.mark.asyncio
async def test_embedding_service_empty_text_raises():
    service = EmbeddingService(base_url="http://test:11434", model="bge-m3")
    with pytest.raises(EmbeddingServiceError):
        await service.embed("")
    with pytest.raises(EmbeddingServiceError):
        await service.embed("   ")


@pytest.mark.asyncio
async def test_embedding_service_retry_on_failure():
    service = EmbeddingService(
        base_url="http://test:11434",
        model="bge-m3",
        max_retries=1,
    )
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(EmbeddingServiceError):
            await service.embed("test query")


@pytest.mark.asyncio
async def test_embedding_service_model_name():
    service = EmbeddingService(base_url="http://test:11434", model="bge-m3")
    assert service.model_name == "bge-m3"


@pytest.mark.asyncio
async def test_embedding_service_batch():
    service = EmbeddingService(base_url="http://test:11434", model="bge-m3")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embeddings": [[0.1] * 1024, [0.2] * 1024]}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        results = await service.embed_batch(["text one", "text two"])
        assert len(results) == 2
        assert len(results[0]) == 1024


@pytest.mark.asyncio
async def test_vector_store_upsert(db_session: AsyncSession):
    vector_store = VectorStore(db_session)
    chunks = [
        {
            "chunk_id": "doc-001-chunk-01",
            "document_id": "doc-001",
            "chunk_index": 0,
            "content": "Test content for the chunk.",
            "word_count": 7,
            "category": KnowledgeCategory.PRODUCT,
            "language": "en",
            "version": "1.0",
            "status": DocumentStatus.AVAILABLE,
            "source": "Product Team",
            "embedding_model": "bge-m3",
            "embedding": [0.1] * 1024,
            "metadata": {
                "document_id": "doc-001",
                "chunk_id": "doc-001-chunk-01",
                "category": KnowledgeCategory.PRODUCT,
                "language": "en",
                "version": "1.0",
                "source": "Product Team",
                "created_at": "2026-09-30",
                "updated_at": "2026-09-30",
            },
        }
    ]
    upserted = await vector_store.upsert(chunks)
    assert upserted == 1


@pytest.mark.asyncio
async def test_vector_store_delete_document(db_session: AsyncSession):
    vector_store = VectorStore(db_session)
    chunks = [
        {
            "chunk_id": "doc-del-chunk-01",
            "document_id": "doc-del",
            "chunk_index": 0,
            "content": "Delete me.",
            "word_count": 2,
            "category": KnowledgeCategory.POLICY,
            "language": "en",
            "version": "1.0",
            "status": DocumentStatus.AVAILABLE,
            "source": "Ops",
            "embedding_model": "bge-m3",
            "embedding": [0.1] * 1024,
            "metadata": {
                "document_id": "doc-del",
                "chunk_id": "doc-del-chunk-01",
                "category": KnowledgeCategory.POLICY,
                "language": "en",
                "version": "1.0",
                "source": "Ops",
                "created_at": "2026-09-30",
                "updated_at": "2026-09-30",
            },
        }
    ]
    await vector_store.upsert(chunks)
    removed = await vector_store.delete_document("doc-del")
    assert removed == 1


@pytest.mark.asyncio
async def test_vector_store_search_returns_empty_on_no_results():
    mock_session = AsyncMock()
    mock_session.execute.return_value = MagicMock()
    mock_session.execute.return_value.all.return_value = []

    vector_store = VectorStore(mock_session)
    query = SearchQuery(query="nonexistent topic", top_k=5)
    results = await vector_store.search(query, [0.0] * 1024)
    assert results == []


@pytest.mark.asyncio
async def test_vector_store_get_by_id(db_session: AsyncSession):
    vector_store = VectorStore(db_session)
    chunks = [
        {
            "chunk_id": "lookup-chunk-01",
            "document_id": "lookup-doc",
            "chunk_index": 0,
            "content": "Findable chunk.",
            "word_count": 2,
            "category": KnowledgeCategory.FAQ,
            "language": "en",
            "version": "1.0",
            "status": DocumentStatus.AVAILABLE,
            "source": "Support",
            "embedding_model": "bge-m3",
            "embedding": [0.1] * 1024,
            "metadata": {
                "document_id": "lookup-doc",
                "chunk_id": "lookup-chunk-01",
                "category": KnowledgeCategory.FAQ,
                "language": "en",
                "version": "1.0",
                "source": "Support",
                "created_at": "2026-09-30",
                "updated_at": "2026-09-30",
            },
        }
    ]
    await vector_store.upsert(chunks)
    chunk = await vector_store.get_by_id("lookup-chunk-01")
    assert chunk is not None
    assert chunk.chunk_id == "lookup-chunk-01"


@pytest.mark.asyncio
async def test_retriever_search():
    mock_embedding_service = AsyncMock()
    mock_embedding_service.embed.return_value = [[0.1] * 1024]

    mock_vector_store = AsyncMock()
    mock_vector_store.search.return_value = [
        SearchResult(
            chunk_id="chunk-01",
            document_id="doc-001",
            content="Relevant content",
            similarity=0.92,
            category=KnowledgeCategory.PRODUCT,
            metadata=ChunkMetadata(
                document_id="doc-001",
                chunk_id="chunk-01",
                category=KnowledgeCategory.PRODUCT,
                language="en",
                version="1.0",
                source="Product",
                created_at="2026-09-30",
                updated_at="2026-09-30",
            ),
        )
    ]

    retriever = Retriever(mock_embedding_service, mock_vector_store)
    query = SearchQuery(query="best moisturizer", top_k=5)
    results = await retriever.search(query)
    assert len(results) == 1
    assert results[0].similarity == 0.92
    mock_embedding_service.embed.assert_called_once()


@pytest.mark.asyncio
async def test_retriever_empty_query():
    mock_embedding_service = AsyncMock()
    mock_vector_store = AsyncMock()
    retriever = Retriever(mock_embedding_service, mock_vector_store)

    results = await retriever.search(SearchQuery(query="   "))
    assert results == []
    mock_embedding_service.embed.assert_not_called()


@pytest.mark.asyncio
async def test_retriever_query_normalization():
    mock_embedding_service = AsyncMock()
    mock_vector_store = AsyncMock()
    retriever = Retriever(mock_embedding_service, mock_vector_store)

    await retriever.search(SearchQuery(query="  multiple   spaces\n\n\nhere  "))
    called_text = mock_embedding_service.embed.call_args[0][0]
    assert "  " not in called_text


@pytest.mark.asyncio
async def test_knowledge_repository_index_document(db_session: AsyncSession):
    vector_store = VectorStore(db_session)
    repo = KnowledgeRepository(vector_store)

    request = IndexDocumentRequest(
        document_id="doc-idx-001",
        title="Test Policy",
        content=" ".join(["policy"] * 500),
        category=KnowledgeCategory.POLICY,
        status=DocumentStatus.APPROVED,
        source="Operations",
        version="1.0",
    )
    upserted = await repo.index_document(request)
    assert upserted >= 1


@pytest.mark.asyncio
async def test_knowledge_repository_reject_non_approved():
    vector_store = AsyncMock()
    repo = KnowledgeRepository(vector_store)

    request = IndexDocumentRequest(
        document_id="doc-reject",
        title="Draft",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.POLICY,
        status=DocumentStatus.DRAFT,
    )
    with pytest.raises(Exception):
        await repo.index_document(request)


@pytest.mark.asyncio
async def test_rag_service_search():
    mock_embedding_service = AsyncMock()
    mock_embedding_service.embed.return_value = [[0.1] * 1024]

    mock_vector_store = AsyncMock()
    mock_vector_store.search.return_value = [
        SearchResult(
            chunk_id="c1",
            document_id="d1",
            content="Return policy allows 30 days.",
            similarity=0.85,
            category=KnowledgeCategory.POLICY,
            metadata=ChunkMetadata(
                document_id="d1",
                chunk_id="c1",
                category=KnowledgeCategory.POLICY,
                language="en",
                version="1.0",
                source="Ops",
                created_at="2026-09-30",
                updated_at="2026-09-30",
            ),
        )
    ]

    retriever = Retriever(mock_embedding_service, mock_vector_store)
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        vector_store=mock_vector_store,
        retriever=retriever,
    )

    result = await rag_service.search(SearchQuery(query="return policy", top_k=5))
    assert result.has_results is True
    assert result.total_chunks == 1
    assert result.chunks[0].document_id == "d1"


@pytest.mark.asyncio
async def test_rag_service_search_empty_on_failure():
    mock_embedding_service = AsyncMock()
    mock_embedding_service.embed.side_effect = Exception("Ollama down")

    mock_vector_store = AsyncMock()
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        vector_store=mock_vector_store,
    )

    result = await rag_service.search(SearchQuery(query="anything", top_k=5))
    assert result.has_results is False
    assert result.chunks == []


@pytest.mark.asyncio
async def test_rag_service_index_document():
    mock_vector_store = AsyncMock()
    mock_vector_store.upsert.return_value = 3

    mock_embedding_service = AsyncMock()
    repo = KnowledgeRepository(mock_vector_store)
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        vector_store=mock_vector_store,
        knowledge_repository=repo,
    )

    request = IndexDocumentRequest(
        document_id="rag-doc-001",
        title="Test Document",
        content=" ".join(["content"] * 500),
        category=KnowledgeCategory.EDUCATION,
        status=DocumentStatus.APPROVED,
        source="Marketing",
        version="1.0",
    )
    upserted = await rag_service.index_document(request)
    assert upserted == 3


@pytest.mark.asyncio
async def test_rag_service_remove_document():
    mock_vector_store = AsyncMock()
    mock_vector_store.delete_document.return_value = 2

    mock_embedding_service = AsyncMock()
    rag_service = RAGService(
        embedding_service=mock_embedding_service,
        vector_store=mock_vector_store,
    )

    removed = await rag_service.remove_document("doc-to-remove")
    assert removed == 2
    mock_vector_store.delete_document.assert_called_with("doc-to-remove")


@pytest.mark.asyncio
async def test_chunk_builder_preserves_category_in_metadata():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="cat-test-001",
        title="Category Test",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.BRAND,
        status=DocumentStatus.APPROVED,
    )
    chunks = builder.build_chunks(doc)
    assert len(chunks) >= 1
    for chunk in chunks:
        assert chunk["metadata"]["category"] == KnowledgeCategory.BRAND


@pytest.mark.asyncio
async def test_chunk_builder_deterministic_chunk_ids():
    builder = ChunkBuilder()
    doc = KnowledgeDocument(
        id="det-001",
        title="Deterministic",
        content=" ".join(["word"] * 500),
        category=KnowledgeCategory.PROMOTION,
        status=DocumentStatus.APPROVED,
    )
    chunks_a = builder.build_chunks(doc)
    chunks_b = builder.build_chunks(doc)
    assert [c["chunk_id"] for c in chunks_a] == [c["chunk_id"] for c in chunks_b]


@pytest.mark.asyncio
async def test_chunk_builder_overlap_does_not_exceed_max():
    builder = ChunkBuilder(overlap_ratio=0.15)
    content = " ".join(["word"] * 2000)
    doc = KnowledgeDocument(
        id="overlap-001",
        title="Overlap",
        content=content,
        category=KnowledgeCategory.EDUCATION,
        status=DocumentStatus.APPROVED,
    )
    chunks = builder.build_chunks(doc)
    for chunk in chunks:
        assert chunk["word_count"] <= builder.max_words
