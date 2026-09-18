# API Versioning

---

Document ID: API-DOC-003

Title: API Versioning

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: API

Last Updated: 2026-09-15

---

# Purpose

Defines how API versions are managed.

---

# URL Format

/api/v1/

Example

/api/v1/products

/api/v1/recommendations

---

# Rules

- Breaking changes require a new version.
- Minor improvements remain in the same version.
- Old versions are deprecated before removal.

---

# Current Version

v1

---

# Core Principle

API changes must not unexpectedly break existing clients.