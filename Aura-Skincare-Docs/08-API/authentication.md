# API Authentication

---

Document ID: API-DOC-001

Title: API Authentication

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: API

Last Updated: 2026-09-15

---

# Purpose

Defines how clients authenticate when accessing Aura APIs.

---

# Authentication Method

Bearer Token (JWT)

Authorization:

Bearer <access_token>

---

# Client Types

- Customer Application
- Admin Dashboard
- AI Agents
- Internal Services

---

# Authorization Rules

Customer

- Access only own resources.

Admin

- Access according to assigned role.

AI Agents

- Use service-to-service credentials.

---

# Token Rules

- Access Token: Short-lived
- Refresh Token: Supported
- Expired tokens must be rejected.

---

# Security

- HTTPS required.
- No credentials in URLs.
- Tokens must never be logged.

---

# Core Principle

Every API request must be authenticated before business logic executes.