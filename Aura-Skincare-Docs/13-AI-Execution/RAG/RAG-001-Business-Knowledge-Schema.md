# RAG-001 — Business Knowledge Schema

**Document ID:** RAG-001
**Version:** 1.0
**Status:** Approved
**Owner:** Architecture
**Applies To:** Customer AI, Admin AI, Marketing AI
**Last Updated:** YYYY-MM-DD

---

# 1. Purpose

This document defines the canonical structure of Aura's Business Knowledge.

Business Knowledge is the trusted source of business information that AI agents
may use to answer customer and administrative questions.

The objective is to ensure that every AI response is generated from verified,
approved and version-controlled business information rather than from model
memory or assumptions.

---

# 2. Goals

The Business Knowledge Layer must:

- Provide accurate business information.
- Maintain a single source of truth.
- Support semantic retrieval (RAG).
- Support version control.
- Allow easy updates without changing AI code.
- Scale as the business grows.
- Prevent AI hallucinations.

---

# 3. Scope

## Included

The following information belongs to Business Knowledge.

### Product Knowledge

- Product catalog
- Product descriptions
- Ingredients
- Benefits
- Warnings
- Usage instructions
- Suitable skin types
- Product images metadata

### Company Policies

- Shipping Policy
- Return Policy
- Refund Policy
- Exchange Policy
- Privacy Policy
- Terms & Conditions
- Payment Policy

### Customer Support

- Frequently Asked Questions
- Contact information
- Business hours

### Promotions

- Active promotions
- Coupon rules
- Discount rules
- Campaign descriptions

### Educational Content

- Skin care guides
- Beauty routines
- Ingredient explanations
- Skin concern education

### Brand Information

- Brand descriptions
- Manufacturer details
- Certifications

---

## Excluded

The following data MUST NOT be stored inside Business Knowledge.

- Customer Profile
- Customer Orders
- Cart
- Wishlist
- Session Memory
- Redis Memory
- Chat History
- Analytics
- Logs
- AI Prompts
- Tool Results

These belong to other architecture components.

---

# 4. Knowledge Categories

Every document belongs to exactly one category.

| Category | Description |
|----------|-------------|
| Product | Product information |
| Policy | Company policies |
| FAQ | Frequently asked questions |
| Promotion | Discounts & campaigns |
| Education | Educational articles |
| Brand | Brand information |
| Support | Customer support |

---

# 5. Knowledge Document Structure

Each knowledge document represents one business entity.

Example:

```text
Document

├── id
├── title
├── content
├── category
├── metadata
├── version
├── status
├── created_at
├── updated_at
└── source
```

---

# 6. Metadata Schema

Each document contains searchable metadata.

Required metadata:

| Field | Required |
|--------|----------|
| id | Yes |
| title | Yes |
| category | Yes |
| language | Yes |
| version | Yes |
| status | Yes |
| tags | Yes |
| source | Yes |
| updated_at | Yes |

Optional metadata:

- brand
- product
- country
- sku
- ingredient
- skin_type
- promotion_id
- campaign
- priority

---

# 7. Document Example

```json
{
  "id": "policy-return-001",
  "title": "Return Policy",
  "category": "Policy",
  "language": "en",
  "version": "1.2",
  "status": "approved",
  "tags": [
    "return",
    "refund"
  ],
  "content": "...",
  "updated_at": "2026-09-30",
  "source": "Operations"
}
```

---

# 8. Source of Truth

Business Knowledge may only originate from approved business sources.

Approved sources:

- Product Database
- Admin Dashboard
- Marketing Team
- Operations Team
- Company Policies

Not approved:

- LLM generated text
- Customer messages
- AI assumptions
- External blogs
- Social media comments

---

# 9. Knowledge Lifecycle

Every document follows the same lifecycle.

```text
Draft

↓

Review

↓

Approved

↓

Indexed

↓

Available to AI

↓

Archived
```

Only Approved documents may be indexed.

---

# 10. Versioning Policy

Every knowledge document must contain:

- Version
- Author
- Created Date
- Updated Date
- Approval Status

Whenever business information changes:

Old Version

↓

New Version

↓

Re-index

↓

Deploy

Old versions remain available for auditing.

---

# 11. Validation Rules

Before indexing, every document must pass validation.

Required:

- Valid metadata
- Valid category
- Non-empty content
- Approved status
- Valid language
- Valid version

Invalid documents must never enter the Vector Store.

---

# 12. Ownership

| Area | Owner |
|------|-------|
| Product | Product Team |
| Policies | Operations |
| Promotions | Marketing |
| FAQ | Customer Support |
| Education | Marketing |
| Brand | Product Team |

Architecture owns the schema.

---

# 13. Design Principles

Business Knowledge follows:

- Single Source of Truth
- Read-only for AI
- Version Controlled
- Immutable History
- Metadata Driven
- AI Independent
- Vendor Neutral

---

# 14. Non-Goals

This document does not define:

- Embedding
- Chunking
- Retrieval
- Prompt Engineering
- Context Window
- Customer Memory
- Session Memory

Those are defined in separate RAG documents.

---

# 15. Related Documents

- RAG-002 — Knowledge Indexing Pipeline
- RAG-003 — Chunking Strategy
- RAG-004 — Embedding Strategy
- RAG-005 — Retrieval Strategy
- AI Memory Strategy
- Prompt Architecture

---

# 16. Revision History

| Version | Date | Changes |
|----------|------|----------|
| 1.0 | YYYY-MM-DD | Initial Release |
