# Deployment Diagrams

---

Document ID: SAD-006

Title: Deployment Diagrams

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Production Deployment

```mermaid
flowchart TB

Supabase Cloud

↓

PostgreSQL

↓

FastAPI

↓

LangGraph

↓

Docker Compose
```

---

# Runtime Services

- Supabase Cloud (Managed PostgreSQL)
- FastAPI
- LangGraph Runtime
- Redis
- n8n
- Monitoring
- Backup Service

---

# Future Deployment

- Kubernetes
- Horizontal Scaling
- Load Balancer
- Redis Cache
- Object Storage (Supabase Storage)

---

# Core Principle

Deploy as simply as possible while preserving a clear path for horizontal scaling.