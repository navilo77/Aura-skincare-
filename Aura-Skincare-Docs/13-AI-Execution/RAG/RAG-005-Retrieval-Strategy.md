# RAG-005 — Retrieval Strategy

**Document ID:** RAG-005
**Version:** 1.0
**Status:** Approved
**Owner:** AI Architecture
**Applies To:** Customer AI, Admin AI, Marketing AI
**Last Updated:** YYYY-MM-DD

---

# 1. Purpose

This document defines how Aura retrieves Business Knowledge from the Vector
Store during Retrieval-Augmented Generation (RAG).

The retrieval strategy is responsible for selecting the most relevant
knowledge before the Large Language Model (LLM) generates a response.

Its primary objective is to maximize answer accuracy while minimizing
hallucinations.

---

# 2. Goals

The retrieval system must:

- Retrieve relevant knowledge.
- Ignore unrelated documents.
- Minimize hallucinations.
- Support metadata filtering.
- Support multilingual search.
- Maintain low latency.
- Scale with business growth.
- Follow KISS and YAGNI principles.

---

# 3. High-Level Retrieval Flow

Customer Question

↓

Query Normalization

↓

Embedding Generation

↓

Vector Search

↓

Metadata Filtering

↓

Similarity Ranking

↓

Top-K Selection

↓

Prompt Assembly

↓

Gemini

↓

Final Response

---

# 4. Query Processing

Before searching, the query is normalized.

Examples

- Remove duplicate spaces
- Normalize Unicode
- Normalize punctuation
- Preserve customer intent

No translation occurs unless explicitly required.

---

# 5. Query Embedding

The normalized query is converted into an embedding.

Model

```
BAAI/bge-m3
```

Server

```
Ollama
```

The query embedding must use the same model that created the stored vectors.

---

# 6. Vector Search

Search is performed against

```
Supabase PostgreSQL

+

pgvector
```

The search returns candidate chunks based on vector similarity.

---

# 7. Metadata Filtering

Before ranking, metadata filters may be applied.

Supported filters:

- Language
- Category
- Brand
- Product
- Skin Type
- Promotion
- Status

Example

Customer asks

```
Shipping Policy
```

Search only

```
Category = Policy
```

instead of searching the entire knowledge base.

---

# 8. Similarity Threshold

Aura ignores documents below the minimum similarity threshold.

Default

```
0.75
```

Meaning

Similarity < 0.75

↓

Ignore

This reduces hallucination risk.

Thresholds may be tuned after production monitoring.

---

# 9. Top-K Selection

Aura returns only the highest-ranking chunks.

Default

```
Top 5
```

Maximum

```
Top 10
```

Reason

Too many chunks increase token usage and reduce answer quality.

---

# 10. Ranking Strategy

Ranking order

1. Similarity Score
2. Metadata Match
3. Document Priority
4. Latest Version

Higher priority documents always rank above archived documents.

---

# 11. Prompt Assembly

Retrieved chunks are injected into the prompt.

Prompt structure

System Prompt

↓

Business Knowledge

↓

Customer Memory

↓

Session Memory

↓

Current Question

↓

Gemini

The LLM never searches the Vector Store directly.

---

# 12. No Result Strategy

If no chunk satisfies the threshold

↓

Do NOT guess

↓

Return

"I couldn't find verified business information."

↓

Suggest escalation if necessary.

Aura prioritizes honesty over speculation.

---

# 13. Retrieval Performance

Target

| Metric | Target |
|---------|---------|
| Query Embedding | <300 ms |
| Vector Search | <150 ms |
| Metadata Filter | <50 ms |
| Ranking | <20 ms |
| Total Retrieval | <500 ms |

---

# 14. Security

Retrieval may access

✓ Business Knowledge

Retrieval may NOT access

✗ Customer Password

✗ Payment Information

✗ Orders

✗ Redis

✗ Session Storage

✗ Admin Secrets

Business Knowledge remains read-only.

---

# 15. Failure Handling

If retrieval fails

↓

Retry once

↓

Still fails

↓

Log Error

↓

Return safe fallback

↓

Continue conversation

The AI must never fabricate business information.

---

# 16. Monitoring

Track

- Search Latency
- Average Similarity Score
- Top-K Distribution
- Empty Search Rate
- Retrieval Success Rate
- Query Volume
- Failed Searches

These metrics help improve retrieval quality over time.

---

# 17. Future Enhancements

Future versions may include

- Hybrid Search
- BM25 + Vector Search
- Cross-Encoder Re-ranking
- Personalized Retrieval
- Image Retrieval
- PDF Retrieval
- Multi-modal Search

These are intentionally out of scope for MVP.

---

# 18. Non-Goals

This document does not define

- Embedding Model
- Chunking
- Business Schema
- Prompt Templates
- Customer Memory

These are defined in separate architecture documents.

---

# 19. Related Documents

- RAG-001 — Business Knowledge Schema
- RAG-002 — Knowledge Indexing Pipeline
- RAG-003 — Chunking Strategy
- RAG-004 — Embedding Strategy
- Prompt Architecture
- Memory Strategy

---

# 20. Revision History

| Version | Date | Changes |
|----------|------|----------|
| 1.0 | YYYY-MM-DD | Initial Release |