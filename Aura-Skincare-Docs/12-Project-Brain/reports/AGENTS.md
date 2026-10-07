# Aura Skincare - Agent Guide

## Source of Truth

**Aura-Skincare-Docs/** is the single source of truth for requirements, architecture, schemas, APIs, database design, AI contracts, automation workflows, security policy, and implementation standards. Always read the relevant approved documents before implementation.

## Pre-Work Checklist

1. Read the relevant Aura-Skincare-Docs sections before writing or changing code.
2. Use Graphify when project-wide knowledge or cross-module context is needed.
3. Confirm the requested behavior exists in approved documentation.
4. Do not invent requirements, APIs, schemas, or business rules.

## Hard Rules

- Never change approved architecture without explicit approval.
- Do not modify documentation unless explicitly requested.
- Treat security, secrets, credentials, and production configuration as sensitive. Never log, expose, or commit them.
- Before major changes, explain the affected documents and the implementation plan.
- Prefer small, reviewable changes over large rewrites.
- Run relevant tests and validation before declaring work complete.

## Documentation-First Workflow

- Every feature, API, database entity, and AI agent must be documented before implementation.
- No implementation begins without approved architecture.
- Create new documents from templates in `Aura-Skincare-Docs/99-Templates/` when needed.

## Tech Stack

- Architecture: Modular Monolith
- Backend: FastAPI (Python)
- Database: PostgreSQL with SQLAlchemy
- AI: LangGraph
- Automation: n8n
- Deployment: Docker Compose
- Frontend: Next.js
- Auth: JWT

## Branching Strategy

- `main` → Production-ready code
- `develop` → Active development
- Feature branches: `feature/<feature-name>`
- Fix branches: `fix/<issue-name>`
- Hotfix branches: `hotfix/<issue-name>`
- All merges require pull request, code review, and passing CI.

## Naming Conventions

- Tables and columns: `snake_case`
- Variables and functions: language-standard casing
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Indexes: `idx_<table>_<column>`
- Unique constraints: `uq_<table>_<column>`
- Foreign keys: `<referenced_entity>_id`

## Coding Standards

- Write clean, readable, maintainable code.
- Follow SOLID principles and single-responsibility functions.
- Handle errors gracefully; never expose internal stack traces.
- Log errors with timestamp, request ID, user ID, module, severity, and error code.
- Never hardcode secrets or prompts in business logic.
- AI responses must pass business-rule validation before being returned.
- Public functions should include comments or docstrings.

## Module Boundaries

Core modules: Customer, Product, Inventory, Order, Payment, AI, Analytics, Notification, Integration, Admin.

- Dependencies point inward toward the business domain.
- No circular dependencies.
- No UI to Database access.
- No AI Agent to Database access.
- Analytics has read-only access.

## Database Rules

- UUID primary keys.
- Soft delete by default (`deleted_at`).
- Foreign key constraints are mandatory unless explicitly justified.
- Schema changes require documentation before migration.
- Indexes based on query patterns.

## Testing

Every production release must validate:
- Functional correctness
- No unresolved critical defects
- Security validation
- Approved acceptance criteria

Test levels: unit, integration, system, acceptance, performance, security, AI testing.

## Security

- Zero Trust architecture.
- Least privilege access.
- Encrypt sensitive data where appropriate.
- Secret access must be logged; secret values must never appear in logs.
- Rotate secrets immediately after compromise and periodically per policy.

## Review Process

- Author → Peer Review → Domain Review → Approval → Publication
- No document may be marked Approved without review.
- Review outcomes: Approved, Approved with Changes, Changes Required, Rejected.

## Governance

- Documents use Document IDs with category prefixes (PRD, SAD, API, SEC, TEST, GOV, etc.).
- Follow Semantic Versioning: MAJOR.MINOR.PATCH.
- Archive deprecated documents.
- Update related documents when changes occur.

## AI Development Rules

- AI is a first-class system component, not an add-on.
- AI never guesses; all responses are based on verified knowledge.
- Final decisions remain with humans.
- Read prompts from managed prompt configuration, not hardcoded in business logic.
- Support human-in-the-loop workflows where applicable.

## Error Handling

- Client errors: 400, 401, 403
- Business errors: 409, 422
- Server errors: 500, 502, 503
- Retry AI Provider, Payment Verification, Courier Status, and Notification Delivery up to 3 times with exponential backoff.
- Graceful degradation; never corrupt business data.

## Observability

- Structured logging.
- Health checks.
- Metrics collection.
- Every critical operation must be measurable, traceable, and logged.

## Core Principles

- Documentation First
- Architecture First
- Single Source of Truth
- API First
- AI First
- Security by Design
- Modular Monolith First
- Observability by Default
- Fail Gracefully
- Backward Compatibility
- Customer Trust First
- Evidence Before Recommendation
- Skin Health Before Sales
- Automation Before Repetition
- Privacy By Design
