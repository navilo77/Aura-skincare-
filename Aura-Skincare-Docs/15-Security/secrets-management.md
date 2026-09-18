15-Security/secrets-management.md
````markdown
# Secrets Management

---

Document ID: SEC-004

Title: Secrets Management

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Security

Last Updated: 2026-09-15

---

# Purpose

Defines how sensitive credentials and secrets are securely stored, accessed, rotated, and retired.

---

# Secrets Covered

- Database Passwords
- JWT Secret Keys
- API Keys
- AI Provider Keys
- Payment Gateway Credentials
- Email Credentials
- OAuth Client Secrets

---

# Storage Rules

- Never store secrets in source code.
- Never commit secrets to Git.
- Use environment variables or a dedicated secrets manager.
- Encrypt secrets at rest.

---

# Access Control

- Least privilege access.
- Authorized personnel only.
- Service accounts receive only required secrets.

---

# Rotation Policy

Rotate secrets:

- Immediately after compromise
- Periodically according to security policy
- After administrator changes

---

# Logging

- Secret access should be logged.
- Secret values must never appear in logs.

---

# Core Principle

Secrets are assets and must be protected like production data.