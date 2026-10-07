from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.knowledge.exceptions import (
    DocumentNotFoundError,
)
from app.modules.knowledge.models.knowledge_chunk import KnowledgeChunk
from app.modules.knowledge.schemas.knowledge import KnowledgeDocument

logger = logging.getLogger(__name__)


class KnowledgeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_document(self, document: KnowledgeDocument) -> KnowledgeChunk:
        chunk = KnowledgeChunk(
            document_id=document.id,
            chunk_id=f"{document.id}-chunk-01",
            chunk_index=0,
            content=document.content,
            word_count=len(document.content.split()),
            category=document.category,
            language=document.language,
            version=document.version,
            status=document.status,
            source=document.source,
            chunk_metadata=None,
        )
        self._session.add(chunk)
        await self._session.flush()
        await self._session.refresh(chunk)
        return chunk

    async def get_document(self, document_id: str) -> KnowledgeChunk | None:
        stmt = (
            select(KnowledgeChunk)
            .where(KnowledgeChunk.document_id == document_id)
            .order_by(KnowledgeChunk.chunk_index)
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_documents(self) -> list[KnowledgeChunk]:
        stmt = (
            select(KnowledgeChunk)
            .where(KnowledgeChunk.chunk_index == 0)
            .order_by(KnowledgeChunk.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_document(
        self, document_id: str, **kwargs: Any
    ) -> KnowledgeChunk | None:
        chunk = await self.get_document(document_id)
        if chunk is None:
            raise DocumentNotFoundError(f"Document '{document_id}' not found")
        for key, value in kwargs.items():
            if hasattr(chunk, key):
                setattr(chunk, key, value)
        await self._session.flush()
        await self._session.refresh(chunk)
        return chunk

    async def delete_document(self, document_id: str) -> bool:
        stmt = select(KnowledgeChunk).where(KnowledgeChunk.document_id == document_id)
        result = await self._session.execute(stmt)
        chunks = result.scalars().all()
        for chunk in chunks:
            await self._session.delete(chunk)
        await self._session.flush()
        return len(chunks) > 0
