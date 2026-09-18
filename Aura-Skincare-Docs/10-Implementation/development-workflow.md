# Development Workflow

---

Document ID: IMP-005

Title: Development Workflow

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Implementation

Last Updated: 2026-09-15

---

# Purpose

Defines the standard workflow for implementing new features.

---

# Workflow

1. Define Requirement (PRD)
2. Approve Feature
3. Update Database Schema via Alembic (if required)
4. Define API Contract
5. Implement Code
6. Write Tests
7. Validate Feature
8. Code Review
9. Merge to Develop
10. Deploy to Staging (Supabase)
11. Business Acceptance
12. Release to Production

---

# Definition of Done

A feature is complete when:

- Code implemented
- Tests passed
- Documentation updated
- API updated
- Database migration applied via Alembic
- Approved by Product Owner

---

# Core Principle

Documentation First → Implementation → Validation → Deployment