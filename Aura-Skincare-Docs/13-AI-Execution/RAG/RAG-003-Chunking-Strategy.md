# RAG-003 — Chunking Strategy

**Document ID:** RAG-003
**Version:** 1.0
**Status:** Approved
**Owner:** Architecture
**Applies To:** Business Knowledge Layer
**Last Updated:** YYYY-MM-DD

---

# 1. Purpose

This document defines how Business Knowledge is divided into semantic chunks
before embedding generation.

Chunking directly affects retrieval quality, AI accuracy and retrieval speed.

The objective is to produce meaningful chunks that preserve context while
remaining small enough for efficient semantic search.

---

# 2. Goals

The chunking strategy must:

- Preserve semantic meaning
- Minimize context loss
- Avoid duplicate information
- Improve retrieval precision
- Support metadata filtering
- Support incremental re-indexing
- Keep implementation simple (KISS)

---

# 3. Design Principles

Aura follows:

- Semantic First
- Metadata Driven
- Document Independent
- Language Independent
- Deterministic
- Version Controlled

---

# 4. Chunking Flow

Document

↓

Normalize

↓

Split

↓

Validate

↓

Attach Metadata

↓

Ready for Embedding

---

# 5. Chunk Types

Aura supports different chunk types.

## Product

One logical section per chunk.

Example

- Description
- Benefits
- Ingredients
- Usage
- Warnings

---

## FAQ

One question-answer pair per chunk.

Example

Question

↓

Answer

↓

Chunk

---

## Policy

Split by headings.

Example

Shipping Policy

↓

Domestic Shipping

↓

Chunk

International Shipping

↓

Chunk

---

## Educational Content

Split by topic.

Example

Acne

↓

Causes

↓

Chunk

Treatment

↓

Chunk

Routine

↓

Chunk

---

# 6. Chunk Size

Default target

```
400–600 words
```

Maximum

```
800 words
```

Minimum

```
150 words
```

Reason

Large chunks reduce retrieval accuracy.

Very small chunks lose context.

---

# 7. Chunk Overlap

Default overlap

```
15%
```

Purpose

Prevent context loss across adjacent chunks.

Example

Chunk A

```
Sentence 1

Sentence 2

Sentence 3

Sentence 4
```

Chunk B begins with

```
Sentence 4

Sentence 5

Sentence 6
```

---

# 8. Chunk Boundaries

Never split inside

- Bullet list
- Table
- Product specification
- FAQ pair
- Code block
- Markdown heading

Prefer splitting at

- Heading
- Paragraph
- Section
- Topic change

---

# 9. Metadata

Every chunk contains metadata.

Required

```json
{
    "document_id": "...",
    "chunk_id": "...",
    "category": "...",
    "language": "...",
    "version": "...",
    "source": "...",
    "created_at": "...",
    "updated_at": "..."
}
```

Optional

- brand
- sku
- ingredient
- skin_type
- tags

---

# 10. Chunk ID Strategy

Each chunk receives a deterministic ID.

Example

```
policy-return-001

↓

chunk-01

↓

policy-return-001-chunk-01
```

Changing the document version creates new chunk IDs.

---

# 11. Validation Rules

Every chunk must satisfy:

✓ Not empty

✓ Valid UTF-8

✓ Metadata attached

✓ Within size limits

✓ Approved source

✓ Valid language

Invalid chunks are rejected.

---

# 12. Re-index Policy

Re-index only changed chunks.

Document

↓

Chunk 4 updated

↓

Delete old Chunk 4

↓

Generate new Chunk 4

↓

Keep remaining chunks

Entire documents should not be re-indexed unless required.

---

# 13. Performance Targets

| Metric | Target |
|---------|---------|
| Chunk Creation | <100 ms |
| Metadata Attachment | <20 ms |
| Validation | <50 ms |
| Re-index | Changed chunks only |

---

# 14. Examples

## Good Chunk

```
Product Name

Benefits

Ingredients

Usage

Warnings
```

---

## Bad Chunk

```
Half of Product A

+

Half of Shipping Policy

+

Random FAQ
```

Never mix unrelated topics.

---

# 15. Future Enhancements

Future versions may support

- Adaptive Chunking
- AI-assisted Chunking
- Table-aware Chunking
- Image-aware Chunking
- PDF Layout Chunking
- Multi-language Chunking

Current MVP intentionally avoids additional complexity (YAGNI).

---

# 16. Non-Goals

This document does not define

- Embedding Model
- Vector Store
- Retrieval
- Prompt Construction

These are defined separately.

---

# 17. Related Documents

- RAG-001 Business Knowledge Schema
- RAG-002 Knowledge Indexing Pipeline
- RAG-004 Embedding Strategy
- RAG-005 Retrieval Strategy

---

# 18. Revision History

| Version | Date | Changes |
|----------|------|----------|
| 1.0 | YYYY-MM-DD | Initial Release |