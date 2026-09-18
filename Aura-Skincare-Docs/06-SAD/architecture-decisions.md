# Architecture Decisions

---

Document ID: SAD-012

Title: Architecture Decisions

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Architecture Decisions

Last Updated: 2026-09-15

---

# ADR Index

## ADR-001

Decision

Use Modular Monolith Architecture

Status

Approved

Reason

Fast MVP with future microservice migration.

---

## ADR-002

Decision

Use FastAPI

Status

Approved

Reason

High performance and excellent AI ecosystem.

---

## ADR-003

Decision

Use LangGraph

Status

Approved

Reason

Multi-agent orchestration and workflow support.

---

## ADR-004

Decision

Use Supabase (Managed PostgreSQL)

Status

Approved

Reason

Supabase provides managed PostgreSQL with built-in backup, monitoring, high availability, and future Storage/Auth/Realtime capabilities while maintaining PostgreSQL compatibility.

---

## ADR-005

Decision

Use Documentation-First Development

Status

Approved

Reason

Ensures traceability and architectural consistency.

---

## ADR-006

Decision

Use Docker Compose for MVP Deployment

Status

Approved

Reason

Simple operations with a clear migration path to Kubernetes.

---

# Change Policy

Any architecture change requires:

- Architecture review
- Impact analysis
- ADR update
- Version increment
- Approval

---

# Core Principle

Every significant architecture decision must be documented, justified, approved, and traceable.