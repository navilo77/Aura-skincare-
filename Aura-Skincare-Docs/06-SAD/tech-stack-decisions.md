# Technology Stack Decisions

---

Document ID: SAD-002

Title: Technology Stack Decisions

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Purpose

This document records the official technology stack decisions for the Aura platform.

Each technology has been selected based on simplicity, maintainability, scalability, community support, and long-term growth.

---

# Architecture Pattern

## Selected

Modular Monolith

## Why

- Simple to develop
- Easy to understand
- Faster MVP delivery
- Lower infrastructure cost
- Easier debugging
- Clean separation of modules
- Supports future migration to Microservices

## Future Upgrade

Microservices (when business growth requires it)

---

# Backend Framework

## Selected

FastAPI

## Why

- Excellent Python ecosystem
- High performance
- Automatic OpenAPI documentation
- Native async support
- Strong typing with Pydantic
- Ideal for AI applications

---

# Programming Language

## Selected

Python

## Why

- Best ecosystem for AI and Machine Learning
- Large developer community
- Excellent library support
- Fast development cycle

---

# AI Framework

## Selected

LangGraph

## Why

- Native support for multi-agent workflows
- Stateful conversations
- Human-in-the-loop support
- Long-running workflow capability
- Easy integration with LLM providers

---

# Database Platform

## Selected

Supabase (Managed PostgreSQL)

## Why

- Managed PostgreSQL eliminates operational overhead
- Built-in backup, monitoring, and high availability
- ACID compliant relational database
- Excellent indexing
- JSON support
- Scalable for future growth
- Includes Supabase Storage and future Auth/Realtime capabilities

## Underlying Technology

PostgreSQL

## ORM

### Selected

SQLAlchemy

### Why

- Mature ORM
- Database abstraction
- Migration support
- Strong community adoption

---

# API Style

## Selected

REST API

## Why

- Easy integration
- Well understood
- Excellent tooling
- Suitable for MVP

## Future Consideration

GraphQL (Optional)

---

# Authentication

## Selected

JWT

## Why

- Stateless authentication
- Easy API integration
- Widely adopted

---

# Deployment

## Selected

Docker Compose

## Why

- Simple local development
- Easy deployment
- Low operational complexity
- Ideal for MVP

## Future Upgrade

Kubernetes

---

# Reverse Proxy

## Selected

Nginx

## Why

- High performance
- SSL termination
- Reverse proxy support
- Load balancing capability

---

# Background Jobs

## Selected

n8n

## Why

- Low-code automation
- Business workflow orchestration
- Easy integration with external services

---

# Observability

## Selected

- Structured Logging
- Health Checks
- Metrics Collection

## Future Upgrade

- Prometheus
- Grafana
- OpenTelemetry

---

# Technologies Deferred

The following technologies are intentionally excluded from Version 1.0:

- Redis
- Kafka
- RabbitMQ
- Kubernetes
- Event Sourcing
- CQRS
- Service Mesh

Reason:

They introduce unnecessary operational complexity for the MVP.

The current Modular Monolith architecture preserves a clear migration path should these technologies become necessary.

---

# Decision Principles

Every technology decision must satisfy the following principles:

- Documentation First
- Architecture First
- Simplicity First
- Security First
- AI First
- Scalability Ready
- Cost Efficient
- Maintainable

---

# Core Principle

Choose the simplest technology that solves today's problem while preserving a clear path for tomorrow's growth.