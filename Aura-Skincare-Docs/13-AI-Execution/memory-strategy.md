# Memory Strategy

---

Document ID: AI-004

Title: Memory Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: AI Execution

Last Updated: 2026-09-15

---

# Purpose

Defines how Aura AI manages conversation context and long-term knowledge.

---

# Memory Types

## Session Memory

- Active conversation only.
- Cleared when the session ends.

---

## Customer Memory

Stores customer-specific information such as:

- Skin Type
- Skin Concerns
- Product Preferences
- Purchase History

Only with appropriate authorization and according to privacy policies.

---

## Business Memory

Shared business knowledge:

- Product Catalog
- Business Rules
- Promotions
- FAQs

---

# Memory Priority

1. Current User Request
2. Session Memory
3. Customer Memory
4. Business Knowledge

---

# Rules

- Never invent missing memory.
- Respect privacy requirements.
- Update memory only after successful validation.

---

# Core Principle

Memory should improve personalization without compromising privacy or accuracy.