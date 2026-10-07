from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.modules.knowledge.schemas.knowledge import ChunkMetadata


class SearchQuery(BaseModel):
    query: str
    category: str | None = None
    language: str | None = None
    brand: str | None = None
    product: str | None = None
    skin_type: str | None = None
    promotion_id: str | None = None
    top_k: int = Field(default=5, ge=1, le=10)
    similarity_threshold: float = Field(default=0.75, ge=0.0, le=1.0)
    status: str | None = "available"


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    similarity: float
    category: str
    metadata: ChunkMetadata

    model_config = {"from_attributes": True}


class RetrievalContext(BaseModel):
    query: str
    chunks: list[SearchResult]
    total_chunks: int
    has_results: bool
    empty_message: str = "I couldn't find verified business information."

    model_config = {"from_attributes": True}


class IndexDocumentRequest(BaseModel):
    document_id: str
    title: str
    content: str
    category: str
    language: str = "en"
    version: str = "1.0"
    status: str = "approved"
    tags: list[str] = Field(default_factory=list)
    source: str = ""
    updated_at: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
