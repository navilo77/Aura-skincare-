# Architecture Glossary

---

Document ID: SAD-013

Title: Architecture Glossary

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Purpose

This glossary defines the official architectural terminology used throughout the Aura platform.

All documentation, AI agents, developers, and future contributors must use these definitions consistently.

---

# Core Terms

## API

Application Programming Interface.

A standardized contract through which software components communicate.

---

## Service

A business component responsible for implementing a specific business capability.

Examples:

- Product Service
- Order Service
- Inventory Service

---

## Module

A logical boundary that groups related business capabilities.

Examples:

- Customer Module
- Product Module
- Order Module

Modules communicate only through defined interfaces.

---

## Entity

A business object with a unique identity that persists in the database.

Examples:

- Customer
- Product
- Order
- Payment

---

## Repository

The data access layer responsible for reading and writing entities.

Repositories never contain business logic.

---

## Business Rule

A rule that defines how the business operates.

Examples:

- Out-of-stock products cannot be purchased.
- Payment must be successful before order creation.

Business rules are independent of the user interface.

---

## DTO (Data Transfer Object)

A lightweight object used to transfer data between layers.

DTOs are not database entities.

---

## Domain Model

The representation of real-world business concepts and relationships.

The domain model is independent of technical implementation.

---

## Aggregate

A consistency boundary within the domain model.

Each aggregate has a single Aggregate Root.

Example:

Order

├── Order Items

├── Payment

└── Shipment

---

## AI Agent

An autonomous software component that performs a specialized task.

Aura AI Agents:

- Router AI Agent
- Customer AI Agent
- Admin AI Agent
- Marketing AI Agent
- Development AI Agent

---

## Router Agent

The AI agent responsible for:

- Intent detection
- Context routing
- Agent selection
- Workflow coordination

---

## Workflow

An ordered sequence of business activities.

Example:

Consultation

↓

Recommendation

↓

Cart

↓

Checkout

↓

Order

↓

Delivery

---

## Integration

Communication between Aura and external systems.

Examples:

- Payment Gateway
- Courier API
- Email Service
- Meta APIs

---

## Event

A significant business occurrence.

Examples:

- Order Created
- Payment Completed
- Product Updated

Events may trigger automation.

---

## API Contract

A formal specification describing an API request and response.

API contracts must remain backward compatible.

---

## Agent Contract

A formal specification defining an AI agent's:

- Responsibilities
- Inputs
- Outputs
- Permissions
- Constraints

---

## Single Source of Truth (SSoT)

Each business concept must have exactly one authoritative definition.

Duplicate definitions are prohibited.

---

## Modular Monolith

An application deployed as a single unit while maintaining clear internal module boundaries.

Modules are designed to allow future extraction into microservices.

---

## Architecture Decision Record (ADR)

A documented record explaining an important architecture decision.

Each ADR includes:

- Decision
- Context
- Alternatives
- Consequences

---

## Observability

The capability to understand system health through:

- Logs
- Metrics
- Traces
- Health Checks

---

## Traceability

The ability to trace every implementation back to:

Requirement

↓

Feature

↓

API

↓

Database

↓

Code

↓

Test

---

## Documentation First

Implementation begins only after documentation is approved.

Documentation is considered the primary source of project knowledge.

---

# Naming Conventions

Modules

PascalCase

Example:

ProductModule

---

Services

PascalCase

Example:

OrderService

---

Database Tables

snake_case

Example:

customer_orders

---

API Endpoints

kebab-case

Example:

/api/v1/customer-orders

---

YAML Files

UPPERCASE ID

Examples:

REQ-001.yaml

FEAT-001.yaml

API-001.yaml

---

# Core Principle

A shared vocabulary ensures that developers, AI agents, architects, and stakeholders communicate with precision, consistency, and a common understanding across the entire Aura platform.