from __future__ import annotations

import logging
import re
import unicodedata

from app.modules.ai.services.rag.embedding_service import EmbeddingService
from app.modules.ai.services.rag.exceptions import RetrievalError
from app.modules.ai.services.rag.schemas import SearchQuery, SearchResult
from app.modules.ai.services.rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    async def search(self, query: SearchQuery) -> list[SearchResult]:
        if not query.query or not query.query.strip():
            return []

        normalized = self._normalize_query(query.query)

        try:
            embeddings = await self._embedding_service.embed(normalized)
            if not embeddings:
                return []
            embedding = embeddings[0]
        except Exception as exc:
            logger.error("Query embedding failed: %s", exc)
            raise RetrievalError(f"Query embedding failed: {exc}") from exc

        try:
            results = await self._vector_store.search(query, embedding)
        except Exception as exc:
            logger.error("Vector search failed: %s", exc)
            raise RetrievalError(f"Vector search failed: {exc}") from exc

        return self._rank(results)

    def _normalize_query(self, query: str) -> str:
        query = unicodedata.normalize("NFKC", query)
        query = re.sub(r"[ \t]+", " ", query)
        query = re.sub(r"\n{3,}", "\n\n", query)
        return query.strip()

    def _rank(self, results: list[SearchResult]) -> list[SearchResult]:
        return sorted(results, key=lambda r: r.similarity, reverse=True)
