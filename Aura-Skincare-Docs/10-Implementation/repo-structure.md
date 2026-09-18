# Repository Structure

---

Document ID: IMP-002

Title: Repository Structure

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Implementation

Last Updated: 2026-09-15

---

# Purpose

Defines the official repository organization for the Aura platform.

---

# Root Structure

```
Aura-Skincare-Docs/
Backend/
Frontend/
Infrastructure/
Scripts/
Docs/
```

---

# Rules

- One responsibility per directory.
- Documentation is maintained separately from source code.
- Infrastructure as Code (IaC) is stored under `Infrastructure/`.
- Reusable scripts belong in `Scripts/`.

---

# Core Principle

A predictable repository structure improves collaboration and maintainability.