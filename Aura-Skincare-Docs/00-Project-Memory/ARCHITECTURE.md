---
Document ID: PM-005
Title: Architecture
Version: 1.0
Status: Approved
Owner: Aura Skincare
Category: Project Memory
Last Updated: 2026-09-19
---

# Architecture

## Purpose

Defines the locked architecture for the Aura Skincare project.

## Architecture Pattern

Modular Monolith (LOCKED)

## Technology Stack

- Backend: FastAPI (Python)
- Frontend: Next.js
- Database: PostgreSQL
- Cache: Redis
- Automation: n8n
- Deployment: Docker Compose

## Out of Scope for V1.5

Do NOT include:
- LangGraph
- RAG
- pgvector
- Redis Memory
- Customer AI
- Admin AI
- Marketing AI
- Autonomous Agents

## Rules

- Never change locked architecture without approval.
- Dependencies point inward toward the business domain.
- No circular dependencies.
- No UI to Database access.
