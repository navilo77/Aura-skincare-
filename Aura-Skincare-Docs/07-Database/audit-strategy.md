# Audit Strategy

---

Document ID: DB-008

Title: Audit Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines how changes to business data are tracked.

---

# Required Audit Fields

- created_at
- created_by
- updated_at
- updated_by
- deleted_at
- deleted_by

---

# Audit Events

- Create
- Update
- Delete
- Restore

---

# Logged Information

- User ID
- Timestamp
- Entity
- Entity ID
- Action
- Previous Value
- New Value

---

# Retention

Audit records are immutable and retained according to the Data Retention Policy.

---

# Core Principle

Every business-critical change must be attributable and traceable.