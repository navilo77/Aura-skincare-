from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class KnowledgeCategory:
    PRODUCT = "Product"
    POLICY = "Policy"
    FAQ = "FAQ"
    PROMOTION = "Promotion"
    EDUCATION = "Education"
    BRAND = "Brand"
    SUPPORT = "Support"


class DocumentStatus:
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    INDEXED = "indexed"
    AVAILABLE = "available"
    ARCHIVED = "archived"


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    content: str
    category: str
    language: str = "en"
    version: str = "1.0"
    status: str = DocumentStatus.APPROVED
    tags: list[str] = Field(default_factory=list)
    source: str = ""
    updated_at: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"from_attributes": True}


class ChunkMetadata(BaseModel):
    document_id: str
    chunk_id: str
    category: str
    language: str
    version: str
    source: str
    created_at: str
    updated_at: str
    brand: str | None = None
    sku: str | None = None
    ingredient: str | None = None
    skin_type: str | None = None
    tags: list[str] = Field(default_factory=list)


class KnowledgeChunk(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    embedding: list[float] | None = None
    metadata: ChunkMetadata
    word_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
