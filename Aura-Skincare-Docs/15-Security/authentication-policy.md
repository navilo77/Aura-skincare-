# Authorization Policy

---

Document ID: SEC-002

Title: Authorization Policy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Security

Last Updated: 2026-09-15

---

# Purpose

Defines authorization and access control across the Aura platform.

---

# Authorization Model

Role-Based Access Control (RBAC)

---

# Roles

- Customer
- Admin
- Marketing
- Support
- AI Agent
- System Administrator

---

# Access Rules

Customers

- View own profile
- View own orders
- Manage own cart

Admins

- Manage products
- Manage orders
- View analytics

Marketing

- Create campaigns
- Manage promotions

AI Agents

- Access only approved APIs
- No direct database access

---

# Security Principles

- Least Privilege
- Deny by Default
- Explicit Permission Required

---

# Core Principle

Every request must be authenticated and explicitly authorized.