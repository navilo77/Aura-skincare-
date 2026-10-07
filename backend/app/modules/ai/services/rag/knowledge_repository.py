from __future__ import annotations

import logging
from typing import Any

from app.modules.ai.services.rag.chunk_builder import ChunkBuilder
from app.modules.ai.services.rag.exceptions import (
    ChunkingError,
    RAGServiceError,
    VectorStoreError,
)
from app.modules.ai.services.rag.schemas import IndexDocumentRequest
from app.modules.ai.services.rag.vector_store import VectorStore
from app.modules.knowledge.schemas.knowledge import DocumentStatus, KnowledgeDocument

logger = logging.getLogger(__name__)


class KnowledgeRepository:
    def __init__(
        self,
        vector_store: VectorStore,
        chunk_builder: ChunkBuilder | None = None,
        knowledge_repository: Any | None = None,
    ) -> None:
        self._vector_store = vector_store
        self._chunk_builder = chunk_builder or ChunkBuilder()
        self._knowledge_repository = knowledge_repository

    async def index_document(self, request: IndexDocumentRequest) -> int:
        document = KnowledgeDocument(
            id=request.document_id,
            title=request.title,
            content=request.content,
            category=request.category,
            language=request.language,
            version=request.version,
            status=request.status,
            tags=request.tags,
            source=request.source,
            updated_at=request.updated_at,
            metadata=request.metadata,
        )

        if document.status not in (
            DocumentStatus.APPROVED,
            DocumentStatus.INDEXED,
            DocumentStatus.AVAILABLE,
        ):
            raise RAGServiceError(
                f"Document status '{document.status}' is not eligible for indexing"
            )

        try:
            chunks = self._chunk_builder.build_chunks(document)
        except (ChunkingError, Exception) as exc:
            logger.error("Chunking failed for document %s: %s", document.id, exc)
            raise

        if not chunks:
            return 0

        try:
            upserted = await self._vector_store.upsert(chunks)
        except Exception as exc:
            logger.error(
                "Vector store upsert failed for document %s: %s",
                document.id,
                exc,
            )
            raise VectorStoreError(f"Failed to store chunks: {exc}") from exc

        logger.info("Indexed document %s: %d chunks upserted", document.id, upserted)
        return upserted

    async def remove_document(self, document_id: str) -> int:
        return await self._vector_store.delete_document(document_id)

    async def reindex_document(self, request: IndexDocumentRequest) -> int:
        removed = await self.remove_document(request.document_id)
        logger.info(
            "Removed %d existing chunks for document %s",
            removed,
            request.document_id,
        )
        return await self.index_document(request)
