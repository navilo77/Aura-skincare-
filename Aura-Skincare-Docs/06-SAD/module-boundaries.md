# Module Boundaries

---

Document ID: SAD-007

Title: Module Boundaries

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Purpose

Defines the logical modules of the Modular Monolith and their responsibilities.

---

## Core Modules

- Customer Module
- Product Module
- Inventory Module
- Order Module
- Payment Module
- AI Module
- Analytics Module
- Notification Module
- Integration Module
- Admin Module

---

# Dependency Rules

Customer Module
→ Product Module

Order Module
→ Inventory Module

Order Module
→ Payment Module

AI Module
→ Product Module

AI Module
→ Customer Module

Analytics Module
→ Read-only access

Integration Module
→ External APIs only

---

# Forbidden Dependencies

❌ Product Module → Order Module

❌ Database → API Layer

❌ UI → Database

❌ AI → Database

---

# Core Principle

Each module owns its own business logic and communicates through explicit service interfaces.