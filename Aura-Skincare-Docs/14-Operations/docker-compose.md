14-Operations/docker/docker-compose.md
````markdown
# Docker Compose Standard

---

Document ID: OPS-021

Title: Docker Compose Standard

Version: 1.0.0

Status: Approved

Owner: Aura Skincare

Category: Operations

Last Updated: 2026-09-16

---

# Purpose

Defines the standard for using Docker Compose to develop, test, and operate the Aura platform in local and non-production environments.

---

# Objectives

- Standardize local development.
- Simplify service orchestration.
- Ensure environment consistency.
- Support reproducible deployments.

---

# Scope

Applies to:

- Backend Services
- Frontend
- Database
- Redis
- n8n
- AI Gateway
- Monitoring Stack

---

# Compose File Standards

Recommended files:

- docker-compose.yml
- docker-compose.override.yml
- docker-compose.dev.yml
- docker-compose.prod.yml

---

# Service Naming

Examples:

- aura-api
- aura-web
- aura-db
- aura-redis
- aura-n8n
- aura-ai

Service names must be lowercase and hyphen-separated.

---

# Networking

- Use dedicated bridge networks.
- Avoid unnecessary host networking.
- Expose only required ports.

---

# Volumes

Persistent storage should be used for:

- Database
- Uploaded Files
- n8n Data
- Logs (where applicable)

---

# Environment Variables

Configuration must be loaded from:

- .env
- Docker Secrets (production)

Never hardcode credentials inside compose files.

---

# Health Checks

Every critical service should define a healthcheck.

Examples:

- API
- Database
- Redis
- AI Gateway

---

# Startup Order

Use dependency management to ensure services start in the correct sequence.

Example:

Database

↓

Redis

↓

Backend

↓

AI Services

↓

Frontend

---

# Security

- Run containers as non-root where possible.
- Use read-only filesystems when appropriate.
- Minimize container privileges.

---

# Related Documents

- deployment-strategy.md
- container-security.md
- image-versioning.md

---

# Core Principle

Docker Compose configurations must be consistent, secure, portable, and easy to maintain.