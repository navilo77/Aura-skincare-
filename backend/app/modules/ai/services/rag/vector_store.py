from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from sqlalchemy import desc, literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnElement

from app.modules.ai.services.rag.exceptions import VectorStoreError
from app.modules.ai.services.rag.schemas import SearchQuery, SearchResult
from app.modules.knowledge.models.knowledge_chunk import KnowledgeChunk
from app.modules.knowledge.schemas.knowledge import ChunkMetadata, DocumentStatus

logger = logging.getLogger(__name__)

_EMBEDDING_COLUMN = "embedding"


class VectorStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(self, chunks: list[dict[str, Any]]) -> int:
        if not chunks:
            return 0

        upserted = 0
        for chunk_data in chunks:
            try:
                await self._upsert_one(chunk_data)
                upserted += 1
            except Exception as exc:
                logger.error(
                    "Failed to upsert chunk %s: %s",
                    chunk_data.get("chunk_id"),
                    exc,
                )
        return upserted

    async def delete_document(self, document_id: str) -> int:
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.document_id == document_id)
        result = await self._session.execute(stmt)
        existing = result.scalars().all()

        for chunk in existing:
            await self._session.delete(chunk)

        await self._session.flush()
        return len(existing)

    async def search(
        self, query: SearchQuery, embedding: list[float]
    ) -> list[SearchResult]:
        if not embedding:
            return []

        filters = self._build_filters(query)
        embedding_literal = "[" + ", ".join(str(v) for v in embedding) + "]"

        where_clauses: list[ColumnElement[Any]] = [
            KnowledgeChunk.status == DocumentStatus.AVAILABLE,
            KnowledgeChunk.embedding.is_not(None),
        ]
        for clause in filters:
            where_clauses.append(clause)

        distance_expr = self._cosine_distance_sql(embedding_literal)

        stmt = (
            select(
                KnowledgeChunk,
                distance_expr.label("similarity"),
            )
            .where(*where_clauses)
            .order_by(desc("similarity"))
            .limit(query.top_k)
        )

        try:
            result = await self._session.execute(stmt)
            rows = result.all()
        except Exception as exc:
            logger.error("Vector search failed: %s", exc)
            raise VectorStoreError(f"Vector search failed: {exc}") from exc

        results: list[SearchResult] = []
        for row in rows:
            chunk, similarity = row
            if similarity < query.similarity_threshold:
                continue

            metadata_dict = self._parse_metadata(chunk.chunk_metadata)
            results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    content=chunk.content,
                    similarity=round(float(similarity), 4),
                    category=chunk.category,
                    metadata=self._to_chunk_metadata(chunk, metadata_dict),
                )
            )

        return results

    async def get_by_id(self, chunk_id: str) -> KnowledgeChunk | None:
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.chunk_id == chunk_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, chunk_id: str) -> bool:
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.chunk_id == chunk_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def _upsert_one(self, chunk_data: dict[str, Any]) -> None:
        chunk_id = chunk_data["chunk_id"]
        existing = await self.get_by_id(chunk_id)

        metadata = chunk_data.get("metadata", {})
        embedding = chunk_data.get("embedding")
        metadata_str = json.dumps(metadata) if metadata else None

        if existing is not None:
            existing.content = chunk_data["content"]
            existing.word_count = chunk_data.get("word_count", 0)
            existing.chunk_metadata = metadata_str
            existing.status = chunk_data.get("status", DocumentStatus.AVAILABLE)
            existing.version = chunk_data.get("version", "1.0")
            if embedding is not None:
                existing.embedding = embedding
            existing.updated_at = datetime.utcnow()
        else:
            chunk = KnowledgeChunk(
                document_id=chunk_data["document_id"],
                chunk_id=chunk_id,
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                word_count=chunk_data.get("word_count", 0),
                category=metadata.get("category", ""),
                language=metadata.get("language", "en"),
                version=metadata.get("version", "1.0"),
                status=chunk_data.get("status", DocumentStatus.AVAILABLE),
                source=metadata.get("source", ""),
                embedding_model=chunk_data.get("embedding_model", "bge-m3"),
                embedding=embedding,
                chunk_metadata=metadata_str,
            )
            self._session.add(chunk)

        await self._session.flush()

    def _build_filters(self, query: SearchQuery) -> list[ColumnElement[Any]]:
        filters: list[ColumnElement[Any]] = []
        if query.category:
            filters.append(KnowledgeChunk.category == query.category)
        if query.language:
            filters.append(KnowledgeChunk.language == query.language)
        if query.status:
            filters.append(KnowledgeChunk.status == query.status)
        return filters

    @staticmethod
    def _cosine_distance_sql(embedding_literal: str) -> Any:
        return literal_column(
            f"1 - ({_EMBEDDING_COLUMN} <=> '{embedding_literal}'::vector)"
        )

    @staticmethod
    def _parse_metadata(raw: str | None) -> dict[str, Any]:
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return {}

    @staticmethod
    def _to_chunk_metadata(chunk: KnowledgeChunk, metadata_dict: dict[str, Any]) -> Any:
        return ChunkMetadata(
            document_id=chunk.document_id,
            chunk_id=chunk.chunk_id,
            category=chunk.category,
            language=chunk.language,
            version=chunk.version,
            source=chunk.source,
            created_at=metadata_dict.get("created_at", ""),
            updated_at=metadata_dict.get("updated_at", ""),
            brand=metadata_dict.get("brand"),
            sku=metadata_dict.get("sku"),
            ingredient=metadata_dict.get("ingredient"),
            skin_type=metadata_dict.get("skin_type"),
            tags=metadata_dict.get("tags", []),
        )
