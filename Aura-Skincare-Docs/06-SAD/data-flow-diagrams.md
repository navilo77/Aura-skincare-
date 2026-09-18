# Data Flow Diagrams

---

Document ID: SAD-003

Title: Data Flow Diagrams

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Purpose

This document defines the official data flow across the Aura platform.

It illustrates how requests, data, AI agents, business services, and external integrations interact throughout the system.

---

# DFD-001 — Customer AI Consultation

```mermaid
flowchart LR

Customer --> Website

Website --> FastAPI

FastAPI --> RouterAgent

RouterAgent --> CustomerAgent

CustomerAgent --> ProductService

ProductService --> Supabase

CustomerAgent --> RecommendationEngine

RecommendationEngine --> CustomerAgent

CustomerAgent --> FastAPI

FastAPI --> Website

Website --> Customer
```

---

# DFD-002 — Product Recommendation Flow

```mermaid
flowchart LR

Customer --> CustomerAgent

CustomerAgent --> ProductDatabase

CustomerAgent --> BusinessRules

BusinessRules --> RecommendationEngine

ProductDatabase --> RecommendationEngine

RecommendationEngine --> CustomerAgent

CustomerAgent --> Customer
```

---

# DFD-003 — Shopping Cart Flow

```mermaid
flowchart LR

Customer --> Website

Website --> CartService

CartService --> ProductService

ProductService --> InventoryService

InventoryService --> Supabase

CartService --> Website

Website --> Customer
```

---

# DFD-004 — Checkout and Order Flow

```mermaid
flowchart LR

Customer --> Checkout

Checkout --> OrderService

OrderService --> PaymentGateway

PaymentGateway --> OrderService

OrderService --> InventoryService

OrderService --> CourierService

OrderService --> NotificationService

OrderService --> Supabase

NotificationService --> Customer
```

---

# DFD-005 — AI Agent Routing

```mermaid
flowchart LR

User --> RouterAgent

RouterAgent --> CustomerAgent

RouterAgent --> AdminAgent

RouterAgent --> MarketingAgent

RouterAgent --> DevelopmentAgent

CustomerAgent --> RouterAgent

AdminAgent --> RouterAgent

MarketingAgent --> RouterAgent

DevelopmentAgent --> RouterAgent
```

---

# DFD-006 — Admin Management Flow

```mermaid
flowchart LR

Admin --> AdminDashboard

AdminDashboard --> FastAPI

FastAPI --> AdminAgent

AdminAgent --> ProductService

AdminAgent --> InventoryService

AdminAgent --> AnalyticsService

AnalyticsService --> Supabase

FastAPI --> AdminDashboard
```

---

# DFD-007 — Marketing Automation Flow

```mermaid
flowchart LR

MarketingAgent --> CampaignService

CampaignService --> n8n

n8n --> Email

n8n --> WhatsApp

n8n --> Messenger

CampaignService --> Supabase
```

---

# DFD-008 — Order Tracking Flow

```mermaid
flowchart LR

Customer --> Website

Website --> OrderService

OrderService --> CourierAPI

CourierAPI --> OrderService

OrderService --> Supabase

OrderService --> Customer
```

---

# System Data Flow Summary

Customer Channels

- Website
- Admin Dashboard
- WhatsApp
- Messenger
- Instagram

↓

API Layer

- FastAPI

↓

AI Layer

- Router Agent
- Customer AI Agent
- Admin AI Agent
- Marketing AI Agent
- Development AI Agent

↓

Business Layer

- Product Service
- Customer Service
- Order Service
- Inventory Service
- Analytics Service

↓

Integration Layer

- Payment Gateway
- Courier
- Email
- Meta APIs
- n8n

↓

Data Layer

- Supabase (Managed PostgreSQL)

---

# Design Principles

- Single Source of Truth
- API First
- AI First
- Modular Architecture
- Documentation First
- Stateless API Layer
- Future Microservices Ready

---

# Core Principle

Every request follows a predictable, documented, and traceable path from user interaction to data persistence, ensuring maintainability, scalability, and reliability.