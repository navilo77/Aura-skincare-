from __future__ import annotations

import logging

from app.modules.ai.services.rag.embedding_service import EmbeddingService
from app.modules.ai.services.rag.exceptions import RAGServiceError, RetrievalError
from app.modules.ai.services.rag.knowledge_repository import KnowledgeRepository
from app.modules.ai.services.rag.retriever import Retriever
from app.modules.ai.services.rag.schemas import (
    IndexDocumentRequest,
    RetrievalContext,
    SearchQuery,
)
from app.modules.ai.services.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        retriever: Retriever | None = None,
        knowledge_repository: KnowledgeRepository | None = None,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._retriever = retriever or Retriever(embedding_service, vector_store)
        self._knowledge_repository = knowledge_repository or KnowledgeRepository(
            vector_store
        )

    async def search(self, query: SearchQuery) -> RetrievalContext:
        try:
            results = await self._retriever.search(query)
        except RetrievalError as exc:
            logger.error("RAG retrieval failed: %s", exc)
            return RetrievalContext(
                query=query.query,
                chunks=[],
                total_chunks=0,
                has_results=False,
            )

        return RetrievalContext(
            query=query.query,
            chunks=results,
            total_chunks=len(results),
            has_results=len(results) > 0,
        )

    async def index_document(self, request: IndexDocumentRequest) -> int:
        try:
            return await self._knowledge_repository.index_document(request)
        except RAGServiceError:
            raise
        except Exception as exc:
            logger.error("RAG index_document failed: %s", exc)
            raise RAGServiceError(f"Indexing failed: {exc}") from exc

    async def reindex_document(self, request: IndexDocumentRequest) -> int:
        try:
            return await self._knowledge_repository.reindex_document(request)
        except RAGServiceError:
            raise
        except Exception as exc:
            logger.error("RAG reindex_document failed: %s", exc)
            raise RAGServiceError(f"Re-indexing failed: {exc}") from exc

    async def remove_document(self, document_id: str) -> int:
        try:
            return await self._knowledge_repository.remove_document(document_id)
        except Exception as exc:
            logger.error("RAG remove_document failed: %s", exc)
            raise RAGServiceError(f"Remove document failed: {exc}") from exc
