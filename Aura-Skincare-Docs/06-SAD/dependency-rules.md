# Dependency Rules

---

Document ID: SAD-008

Title: Dependency Rules

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Layered Architecture

```text
Presentation Layer
        ↓
API Layer
        ↓
Business Layer
        ↓
Repository Layer
        ↓
Database
```

---

# Allowed Dependencies

- Presentation → API
- API → Business
- Business → Repository
- Repository → Database

---

# Forbidden Dependencies

- Database → Business
- Database → API
- UI → Database
- Integration → UI
- AI Agent → Database

---

# Design Rules

- No Circular Dependencies
- Single Responsibility Principle
- Dependency Injection
- Interface-based Communication
- Loose Coupling
- High Cohesion

---

# Future Rule

When migrating to Microservices, module interfaces become service contracts without changing business logic.

---

# Core Principle

Dependencies always point inward toward the business domain, never outward.ko