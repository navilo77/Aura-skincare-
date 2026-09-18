# Migration Strategy

---

Document ID: DB-006

Title: Migration Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines how database schema changes are created, reviewed, tested, and deployed.

---

# Migration Tool

- Alembic
- SQLAlchemy
- Supabase (Managed PostgreSQL)

---

# Rules

- Every schema change requires a migration.
- Never edit an existing migration after deployment.
- Each migration must have a rollback strategy.
- One logical change per migration.
- Migrations must be version controlled.

---

# Naming Convention

YYYYMMDDHHMM_description

Examples:

- 202609151230_create_products
- 202609151500_add_inventory_table

---

# Deployment Order

1. Backup database
2. Run migration
3. Validate schema
4. Verify application
5. Monitor logs

---

# Rollback

Rollback is mandatory for production deployments.

---

# Core Principle

Database migrations must be predictable, reversible, and traceable.