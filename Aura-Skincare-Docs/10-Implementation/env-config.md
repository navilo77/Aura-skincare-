# Environment Configuration

---

Document ID: IMP-003

Title: Environment Configuration

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Implementation

Last Updated: 2026-09-15

---

# Purpose

Defines how environment variables are managed.

---

# Environments

- Development
- Staging
- Production

---

# Configuration Rules

- Store secrets in environment variables.
- Never commit `.env` files.
- Maintain `.env.example` in the repository.
- Separate configuration for each environment.

---

# Typical Variables

- DATABASE_URL
- SUPABASE_URL
- SUPABASE_ANON_KEY
- SUPABASE_SERVICE_ROLE_KEY
- REDIS_URL
- AI_PROVIDER
- JWT_SECRET
- PAYMENT_API_KEY
- EMAIL_API_KEY

---

# Core Principle

Configuration belongs to the environment, not the source code.