from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

_EMBEDDING_DIMENSION = 1024


class KnowledgeChunk(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_chunks"

    document_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    chunk_id: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    chunk_index: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(nullable=False, default=0)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0")
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="available", index=True
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    embedding_model: Mapped[str] = mapped_column(
        String(100), nullable=False, default="bge-m3"
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(_EMBEDDING_DIMENSION), nullable=True
    )
    chunk_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_knowledge_chunks_document_category", "document_id", "category"),
        Index("ix_knowledge_chunks_status_category", "status", "category"),
    )
