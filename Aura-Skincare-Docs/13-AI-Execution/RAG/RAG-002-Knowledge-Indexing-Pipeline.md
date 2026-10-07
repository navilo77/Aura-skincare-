# RAG-002 — Knowledge Indexing Pipeline

**Document ID:** RAG-002
**Version:** 1.0
**Status:** Approved
**Owner:** Architecture
**Applies To:** Business Knowledge Layer
**Last Updated:** YYYY-MM-DD

---

# 1. Purpose

This document defines how Business Knowledge enters Aura's Vector Database.

The Knowledge Indexing Pipeline converts approved business documents into
vector embeddings that can later be retrieved by AI agents using semantic
search.

The indexing pipeline is completely independent from the chat pipeline.

---

# 2. Goals

The pipeline must:

- Keep Vector Store synchronized.
- Support incremental indexing.
- Support full re-index.
- Preserve metadata.
- Prevent duplicate vectors.
- Minimize downtime.
- Support future automation.

---

# 3. High-Level Architecture

```

Business Knowledge
(Product / Policy / FAQ)

↓

Validation

↓

Normalization

↓

Chunking

↓

Embedding Generation

↓

Vector Storage

↓

Ready for Retrieval

```

---

# 4. Data Sources

Only approved business data may enter the pipeline.

Supported sources:

- Product Database
- Policy Documents
- FAQ Database
- Markdown Documents
- Admin Dashboard
- Future CMS

Not allowed:

- Customer Chat
- Redis
- Session Memory
- AI Generated Content
- Logs
- Temporary Files

---

# 5. Pipeline Stages

## Stage 1 — Document Collection

Collect approved documents from Business Knowledge.

Requirements:

- Approved
- Latest Version
- Valid Metadata

Output:

```

Business Document

```

---

## Stage 2 — Validation

Every document must pass validation.

Checks:

- ID exists
- Category exists
- Metadata complete
- Version exists
- Language valid
- Content not empty

Invalid documents are rejected.

---

## Stage 3 — Normalization

Normalize content before indexing.

Examples:

- Remove duplicate spaces
- Normalize line endings
- Remove unsupported formatting
- Standardize Unicode

Purpose:

Generate consistent embeddings.

---

## Stage 4 — Chunking

Split documents into semantic chunks.

Chunking rules are defined in:

RAG-003 — Chunking Strategy

Output:

```

Document

↓

Chunk 1

Chunk 2

Chunk 3

```

---

## Stage 5 — Embedding Generation

Each chunk becomes one embedding.

Embedding Model:

```

BAAI/bge-m3

```

Embedding Server:

```

Ollama

```

Output:

```

Chunk

↓

Embedding Vector

```

---

## Stage 6 — Metadata Attachment

Each vector stores metadata.

Example:

```json
{
  "document_id":"policy-return-001",
  "chunk_id":"chunk-03",
  "category":"Policy",
  "language":"en",
  "version":"1.0",
  "updated_at":"2026-09-30"
}
```

Metadata enables filtering during retrieval.

---

## Stage 7 — Vector Storage

Store embedding inside:

Supabase PostgreSQL

with

pgvector

Each row contains:

- Vector
- Metadata
- Chunk Text

---

# 6. Indexing Modes

Aura supports two indexing modes.

## Full Index

Used when:

- First deployment
- Embedding model changes
- Schema changes

Pipeline:

Delete Old Index

↓

Rebuild Everything

---

## Incremental Index

Used when:

- Product updated
- Policy changed
- FAQ modified

Pipeline:

Find Changed Document

↓

Re-index Only Changed Chunks

---

# 7. Update Triggers

Re-index occurs when:

- Product Created
- Product Updated
- Policy Updated
- FAQ Updated
- Promotion Updated

No re-index for:

- Customer Data
- Session Data
- Analytics
- Redis

---

# 8. Duplicate Prevention

Each chunk has a unique identity.

```
Document ID
+
Chunk Number
+
Version
```

If the same version already exists:

Skip indexing.

---

# 9. Failure Handling

Possible failures:

Embedding failure

↓

Retry

↓

Still failed

↓

Mark document as Failed

↓

Log error

↓

Continue remaining documents

The pipeline must never stop because of one failed document.

---

# 10. Monitoring

Track:

- Indexed Documents
- Indexed Chunks
- Failed Documents
- Failed Embeddings
- Processing Time
- Queue Size

---

# 11. Performance Targets

| Metric | Target |
|---------|---------|
| Validation | <50 ms |
| Chunking | <100 ms |
| Embedding | <300 ms / chunk |
| Storage | <100 ms |
| Incremental Index | <5 sec |
| Full Re-index | Background Job |

---

# 12. Security

The indexing pipeline:

- Cannot access Customer Memory.
- Cannot access Session Memory.
- Cannot modify Business Data.
- Has read-only access to business documents.
- Writes only to the Vector Store.

---

# 13. Future Enhancements

Planned:

- Scheduled Re-index
- Background Workers
- Queue Processing
- Multi-language Documents
- Image Embeddings
- PDF Knowledge
- Video Knowledge
- Automatic CMS Sync

---

# 14. Non-Goals

This document does not define:

- Chunk Size
- Embedding Model Details
- Retrieval Logic
- Prompt Injection

These are covered in:

- RAG-003
- RAG-004
- RAG-005

---

# 15. Related Documents

- RAG-001 — Business Knowledge Schema
- RAG-003 — Chunking Strategy
- RAG-004 — Embedding Strategy
- RAG-005 — Retrieval Strategy

---

# 16. Revision History

| Version | Date | Changes |
|----------|------|----------|
| 1.0 | YYYY-MM-DD | Initial Release |
