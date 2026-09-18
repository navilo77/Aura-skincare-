# Soft Delete Strategy

---

Document ID: DB-009

Title: Soft Delete Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines how records are logically deleted without permanent removal.

---

# Required Columns

- deleted_at
- deleted_by

---

# Rules

- Business records are soft deleted by default.
- Deleted records are excluded from normal queries.
- Restore operations are supported.
- Permanent deletion requires explicit approval.

---

# Exceptions

Temporary or cache tables may use hard delete.

---

# Benefits

- Data recovery
- Auditability
- Compliance
- Accident prevention

---

# Core Principle

Delete logically first, physically only when required.