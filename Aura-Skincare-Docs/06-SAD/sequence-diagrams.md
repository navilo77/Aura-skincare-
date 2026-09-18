# Sequence Diagrams

---

Document ID: SAD-005

Title: Sequence Diagrams

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Software Architecture

Last Updated: 2026-09-15

---

# Customer AI Consultation

```mermaid
sequenceDiagram

participant Customer
participant Website
participant FastAPI
participant Router
participant CustomerAI
participant ProductService
participant Supabase

Customer->>Website: Ask skincare question

Website->>FastAPI: API Request

FastAPI->>Router: Route Request

Router->>CustomerAI: Consultation

CustomerAI->>ProductService: Get Products

ProductService->>Supabase: Query

Supabase-->>ProductService: Result

ProductService-->>CustomerAI: Products

CustomerAI-->>Router: Recommendation

Router-->>FastAPI: Response

FastAPI-->>Website: JSON Response

Website-->>Customer: Recommendation
```

---

# Checkout Flow

```mermaid
sequenceDiagram

participant Customer
participant Website
participant OrderService
participant PaymentGateway
participant Inventory
participant Courier
participant Notification

Customer->>Website: Checkout

Website->>OrderService: Create Order

OrderService->>PaymentGateway: Payment

PaymentGateway-->>OrderService: Success

OrderService->>Inventory: Reserve Stock

OrderService->>Courier: Delivery Request

OrderService->>Notification: Confirmation

Notification-->>Customer: Order Confirmed
```

---

# Core Principle

Every business process follows a predictable, traceable sequence.