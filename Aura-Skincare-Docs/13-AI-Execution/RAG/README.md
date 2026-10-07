# RAG Documentation
# Aura AI RAG Architecture

**Document ID:** RAG-README  
**Version:** 1.0  
**Status:** Approved  
**Owner:** Aura Architecture Team  
**Last Updated:** 2026-09-30

---

# Overview

This directory contains the official Retrieval-Augmented Generation (RAG) architecture documentation for the Aura AI platform.

The RAG layer enables Aura AI to retrieve verified business knowledge before generating responses. Instead of relying solely on the LLM, the AI grounds its answers using trusted information stored in Aura's Business Knowledge Base.

This architecture is designed to provide:

- Accurate responses
- Reduced hallucinations
- Consistent recommendations
- Fast semantic search
- Long-term maintainability
- Enterprise scalability

---

# Goals

The RAG architecture exists to:

- Provide trustworthy business knowledge to AI agents.
- Keep business knowledge separate from application logic.
- Enable semantic search over products, FAQs, policies, and educational content.
- Support Customer AI, Admin AI, and Marketing AI through a shared knowledge layer.
- Allow knowledge updates without changing application code.

---

# Scope

This directory defines the complete Business Knowledge Retrieval architecture.

Included documents:

| ID | Document |
|----|----------|
| RAG-001 | Business Knowledge Schema |
| RAG-002 | Knowledge Indexing Pipeline |
| RAG-003 | Chunking Strategy |
| RAG-004 | Embedding Strategy |
| RAG-005 | Retrieval Strategy |

The following topics are documented elsewhere:

- Prompt Architecture
- Memory Strategy
- Session Memory
- Customer Memory
- Tool Registry
- Tool Execution Rules
- Context Window Policy
- Agent Communication

---

# Current Architecture Decisions

| Component | Decision |
|------------|----------|
| Chat LLM | Google Gemini |
| AI Framework | LangGraph |
| Embedding Model | BAAI/bge-m3 |
| Embedding Runtime | Ollama (Local) |
| Session Memory | Redis |
| Customer Memory | Supabase PostgreSQL |
| Business Knowledge | Supabase PostgreSQL |
| Vector Store | Supabase pgvector |
| Retrieval Method | Semantic Vector Search |
| Similarity Metric | Cosine Similarity |

---

# High-Level Architecture

```text
Business Knowledge

        │

        ▼

Knowledge Indexing Pipeline

        │

        ▼

Chunking Strategy

        │

        ▼

Embedding Strategy

        │

        ▼

Supabase pgvector

        │

        ▼

Retrieval Strategy

        │

        ▼

Prompt Builder

        │

        ▼

Google Gemini

        │

        ▼

Customer Response
```

---

# Documentation Structure

## RAG-001 — Business Knowledge Schema

Defines:

- Knowledge categories
- Knowledge entities
- Metadata
- Versioning
- Ownership
- Validation
- Storage model

---

## RAG-002 — Knowledge Indexing Pipeline

Defines:

- Data ingestion
- Validation
- Cleaning
- Chunk generation
- Embedding generation
- Metadata generation
- Vector indexing
- Incremental update
- Full re-index
- Failure recovery

---

## RAG-003 — Chunking Strategy

Defines:

- Chunk boundaries
- Chunk size
- Chunk overlap
- FAQ chunking
- Product chunking
- Guide chunking
- Policy chunking
- Markdown handling
- Table handling
- Multi-language strategy

---

## RAG-004 — Embedding Strategy

Defines:

- Embedding model
- Ollama runtime
- Embedding versioning
- Batch embedding
- Cache policy
- Metadata
- Re-index strategy

---

## RAG-005 — Retrieval Strategy

Defines:

- Query embedding
- Semantic search
- Metadata filtering
- Similarity scoring
- Top-K retrieval
- Ranking
- Context assembly
- Empty-result handling

---

# Retrieval Flow

```text
User Question

      │

      ▼

Query Embedding

      │

      ▼

Supabase pgvector Search

      │

      ▼

Top-K Results

      │

      ▼

Metadata Filtering

      │

      ▼

Prompt Builder

      │

      ▼

Google Gemini

      │

      ▼

Final Response
```

---

# Engineering Principles

The Aura AI platform follows a small set of architecture principles to keep the system maintainable, scalable, and easy to understand.

## KISS (Keep It Simple, Stupid)

Always choose the simplest solution that satisfies the current requirements.

Avoid unnecessary abstraction, excessive configuration, and over-engineering.

Examples:

- One embedding model
- One indexing pipeline
- One vector database
- One retrieval pipeline

---

## YAGNI (You Aren't Gonna Need It)

Do not implement features until they are actually required.

Examples:

- No hybrid search until needed.
- No multiple vector databases.
- No multiple embedding providers.
- No cross-encoder reranking for MVP.
- No knowledge graph before there is a business requirement.

Future ideas belong in the roadmap—not in today's architecture.

---

## Separation of Concerns

Every component has a single responsibility.

Example:

Business Knowledge
→ Stores verified business information

Knowledge Indexing
→ Converts knowledge into searchable vectors

Embedding Strategy
→ Generates embeddings

Retrieval Strategy
→ Retrieves relevant knowledge

Prompt Builder
→ Builds the LLM prompt

Gemini
→ Generates the final response

---

## Single Source of Truth (SSoT)

Business information must exist in only one authoritative source.

AI must never invent:

- Product information
- Prices
- Stock
- Discounts
- Policies
- Shipping rules

All business facts must come from the Business Knowledge Layer.

---

## Evidence-Based AI

Whenever possible, AI responses must be grounded in retrieved business knowledge rather than relying on LLM memory.

Retrieved knowledge always takes precedence over model assumptions.

---

## Modularity

Each component should be independently replaceable.

Example:

```text
BAAI/bge-m3

↓

Gemini Embedding

↓

Future Embedding Model
```

Changing one component should not require redesigning the entire architecture.

---

## Vendor Independence

Business logic must remain independent of infrastructure providers.

Current providers:

- Google Gemini
- Ollama
- Supabase
- Redis

Any provider can be replaced without affecting business logic.

---

## Scalability

The architecture should support future growth with minimal changes.

Future extensions include:

- Admin AI
- Marketing AI
- Voice AI
- Image Search
- Hybrid Search
- External Knowledge Sources

---

## Performance First

Optimize for predictable low latency.

Target retrieval latency:

| Operation | Target |
|------------|---------|
| Query Embedding | <100 ms |
| Vector Search | <50 ms |
| Context Assembly | <30 ms |
| Total Retrieval | <200 ms |

---

## Security

The RAG layer is read-only.

It must never:

- Modify customer data
- Update business knowledge
- Delete vectors
- Execute business actions

Its only responsibility is knowledge retrieval.

---

## Readability Over Cleverness

Architecture should be understandable by any engineer joining the project.

Prefer clear designs over clever implementations.

Simple systems are easier to maintain, debug, and extend.

---

# Related Documents

- memory-strategy.md
- prompt-library.md
- router-logic.md
- ai-agent-workflow.md
- hallucination-guardrails.md

---

# Future Roadmap

Potential future enhancements:

- Hybrid Search
- Cross-Encoder Re-ranking
- Image Embeddings
- Multimodal Retrieval
- Knowledge Graph
- External Knowledge Connectors
- Multi-Tenant Knowledge Bases

These features are intentionally deferred until there is a validated business requirement.

---

# Version History

| Version | Date | Description |
|----------|------------|------------------------------|
| 1.0 | 2026-09-30 | Initial RAG Architecture Foundation |
