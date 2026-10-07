from __future__ import annotations

import logging
import re
from typing import Any

from app.modules.ai.services.rag.exceptions import ChunkingError
from app.modules.knowledge.exceptions import DocumentValidationError
from app.modules.knowledge.schemas.knowledge import (
    ChunkMetadata,
    KnowledgeCategory,
    KnowledgeDocument,
)

logger = logging.getLogger(__name__)

_MIN_WORDS = 150
_MAX_WORDS = 800
_TARGET_WORDS_MIN = 400
_TARGET_WORDS_MAX = 600
_OVERLAP_RATIO = 0.15


class ChunkBuilder:
    def __init__(
        self,
        min_words: int = _MIN_WORDS,
        max_words: int = _MAX_WORDS,
        target_words_min: int = _TARGET_WORDS_MIN,
        target_words_max: int = _TARGET_WORDS_MAX,
        overlap_ratio: float = _OVERLAP_RATIO,
    ) -> None:
        self.min_words = min_words
        self.max_words = max_words
        self.target_words_min = target_words_min
        self.target_words_max = target_words_max
        self.overlap_ratio = overlap_ratio

    def build_chunks(self, document: KnowledgeDocument) -> list[dict[str, Any]]:
        if not document.content or not document.content.strip():
            raise DocumentValidationError("Document content is empty")

        if not self._is_valid_category(document.category):
            raise DocumentValidationError(f"Invalid category: {document.category}")

        if document.status not in (
            "approved",
            "indexed",
            "available",
        ):
            raise DocumentValidationError(
                f"Document status '{document.status}' is not eligible for indexing"
            )

        normalized = self._normalize(document.content)
        raw_chunks = self._split(document, normalized)

        chunks = []
        for idx, chunk_text in enumerate(raw_chunks):
            validated = self._validate_chunk(chunk_text)
            if validated is None:
                continue

            chunk_id = f"{document.id}-chunk-{idx + 1:02d}"

            chunk = {
                "chunk_id": chunk_id,
                "document_id": document.id,
                "chunk_index": idx,
                "content": validated,
                "word_count": self._word_count(validated),
                "metadata": ChunkMetadata(
                    document_id=document.id,
                    chunk_id=chunk_id,
                    category=document.category,
                    language=document.language,
                    version=document.version,
                    source=document.source,
                    created_at=document.updated_at,
                    updated_at=document.updated_at,
                    brand=document.metadata.get("brand"),
                    sku=document.metadata.get("sku"),
                    ingredient=document.metadata.get("ingredient"),
                    skin_type=document.metadata.get("skin_type"),
                    tags=document.tags,
                ).model_dump(),
            }
            chunks.append(chunk)

        if not chunks:
            raise ChunkingError("No valid chunks generated from document")

        return chunks

    def _split(self, document: KnowledgeDocument, text: str) -> list[str]:
        category = document.category

        if category == KnowledgeCategory.FAQ:
            return self._split_faq(text)
        if category == KnowledgeCategory.PRODUCT:
            return self._split_product(text)
        if category == KnowledgeCategory.POLICY:
            return self._split_by_headings(text)
        if category == KnowledgeCategory.EDUCATION:
            return self._split_by_topic(text)
        return self._split_generic(text)

    def _split_faq(self, text: str) -> list[str]:
        pairs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in pairs if p.strip()]

    def _split_product(self, text: str) -> list[str]:
        pattern = (
            r"\n(?=(?:Description|Benefits|Ingredients|"
            r"Usage|Warnings|How to Use)\b)"
        )
        sections = re.split(pattern, text, flags=re.IGNORECASE)
        return [
            s.strip()
            for s in sections
            if self._word_count(s) >= self.min_words or len(sections) == 1
        ]

    def _split_by_headings(self, text: str) -> list[str]:
        sections = re.split(r"\n(?=#{1,3}\s|\d+\.\s)", text)
        return [s.strip() for s in sections if s.strip()]

    def _split_by_topic(self, text: str) -> list[str]:
        sections = re.split(r"\n(?=(?:#{1,3}\s|#{1,2}\s|Topic:|##\s))", text)
        return [s.strip() for s in sections if s.strip()]

    def _split_generic(self, text: str) -> list[str]:
        paragraphs = re.split(r"\n\s*\n", text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        chunks: list[str] = []
        current: list[str] = []
        current_words = 0

        for para in paragraphs:
            para_words = self._word_count(para)
            if para_words > self.max_words:
                if current:
                    chunks.append("\n\n".join(current))
                    current = []
                    current_words = 0
                chunks.extend(self._split_large_paragraph(para))
                continue

            if current_words + para_words > self.max_words and current:
                chunk_text = "\n\n".join(current)
                chunks.append(chunk_text)
                overlap_size = self._overlap_size(chunk_text)
                if overlap_size > 0 and len(chunks) > 0:
                    current = [chunks[-1][-overlap_size:].strip(), para]
                else:
                    current = [para]
                current_words = sum(self._word_count(p) for p in current)
            else:
                current.append(para)
                current_words += para_words

        if current:
            last = "\n\n".join(current)
            last_words = self._word_count(last)
            if self.target_words_min <= last_words <= self.max_words or not chunks:
                chunks.append(last)
            elif chunks and last_words < self.target_words_min:
                chunks[-1] = chunks[-1] + "\n\n" + last

        return [c for c in chunks if c.strip()]

    def _split_large_paragraph(self, text: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: list[str] = []
        current: list[str] = []
        current_words = 0

        for sentence in sentences:
            sentence_words = self._word_count(sentence)
            if current_words + sentence_words > self.max_words and current:
                chunks.append(" ".join(current))
                overlap_size = self._overlap_size(" ".join(current))
                if overlap_size > 0:
                    overlap_text = " ".join(current)
                    current = [overlap_text[-overlap_size:].strip(), sentence]
                else:
                    current = [sentence]
                current_words = sum(self._word_count(s) for s in current)
            else:
                current.append(sentence)
                current_words += sentence_words

        if current:
            chunks.append(" ".join(current))

        return chunks if chunks else [text]

    def _validate_chunk(self, text: str) -> str | None:
        text = text.strip()
        if not text:
            return None
        word_count = self._word_count(text)
        if word_count < self.min_words:
            return None
        if word_count > self.max_words:
            return self._truncate(text)
        return text

    def _truncate(self, text: str) -> str:
        words = text.split()
        return " ".join(words[: self.max_words])

    def _overlap_size(self, text: str) -> int:
        return int(self._word_count(text) * self.overlap_ratio)

    @staticmethod
    def _word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def _is_valid_category(category: str) -> bool:
        valid = {
            KnowledgeCategory.PRODUCT,
            KnowledgeCategory.POLICY,
            KnowledgeCategory.FAQ,
            KnowledgeCategory.PROMOTION,
            KnowledgeCategory.EDUCATION,
            KnowledgeCategory.BRAND,
            KnowledgeCategory.SUPPORT,
        }
        return category in valid
