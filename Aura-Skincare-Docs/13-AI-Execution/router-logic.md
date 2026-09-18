# Router Logic

---

Document ID: AI-003

Title: Router Logic

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: AI Execution

Last Updated: 2026-09-15

---

# Purpose

Defines how incoming requests are routed to the correct AI agent.

---

# Routing Rules

Customer Questions

→ Customer AI

Administration

→ Admin AI

Marketing Content

→ Marketing AI

Development Tasks

→ Development AI

Unknown Intent

→ Ask clarifying question

---

# Fallback

If confidence is below threshold:

- Request clarification
- Do not guess

---

# Core Principle

The correct agent should answer the correct request.