# Backend Completion Plan - Aura Skincare

## Overview
Complete all backend modules from stubs to production-ready implementations.

---

## Phase 1: Critical Path (Payment + Notification) - Week 1

### 1.1 Payment Module (Stripe)
**Files to create:**
- `models/payment.py` - Payment, PaymentMethod, Refund models
- `schemas/payment.py` - Request/response schemas
- `repositories/payment.py` - CRUD operations
- `services/payment.py` - Stripe integration, webhook handling
- `routes/payment.py` - REST endpoints
- `integrations/payment/stripe.py` - Stripe client wrapper

**Endpoints:**
- `POST /api/v1/payments/intent` - Create payment intent
- `POST /api/v1/payments/confirm` - Confirm payment
- `POST /api/v1/payments/webhook` - Stripe webhook
- `POST /api/v1/payments/{id}/refund` - Refund payment
- `GET /api/v1/payments/methods` - List payment methods

### 1.2 Notification Delivery
**Files to modify/create:**
- `services/delivery.py` - Email/SMS/Push delivery with retry
- `integrations/email/sendgrid.py` - SendGrid provider
- `integrations/n8n/webhook.py` - n8n webhook caller
- `routes/preference.py` - User notification preferences
- Add `notification_queue` table for async processing

**Features:**
- Exponential backoff retry (3 attempts)
- Template rendering with Jinja2
- Channel routing (email/SMS/push)
- Delivery status tracking

---

## Phase 2: Business Automation - Week 2

### 2.1 Order Automation
**Files to create:**
- `services/n8n_client.py` - n8n workflow trigger
- `tasks/order_tasks.py` - Celery/async tasks for order events
- `validators/order.py` - Complete validation logic
- `models/workflow.py` - Workflow execution tracking

**Workflows to implement:**
- Order confirmation → notification + inventory reservation
- Payment success → fulfillment trigger
- Inventory low → reorder notification
- Abandoned cart → recovery email

### 2.2 Marketing AI
**Files to create:**
- `services/generation.py` - AI content generation (LangChain/LangGraph)
- `integrations/storage/s3.py` - Asset storage
- `services/scheduler.py` - Campaign scheduling
- `prompts/` - Prompt templates for each content type

---

## Phase 3: Platform Hardening - Week 3

### 3.1 Admin RBAC & Audit
- Permission-based route guards
- Audit log model + middleware
- Bulk operations (import/export)

### 3.2 AI Agents (LangGraph)
- Define agent graphs in `modules/ai/agents/`
- Tool registry + execution
- Human-in-the-loop checkpoints

### 3.3 Integrations
- Email: SendGrid + template management
- WhatsApp: Twilio/Gupshup
- SEO: Meta tags, sitemap generation
- Scrapling: Product data enrichment

### 3.4 Memory System
- Redis backend for session/business/customer memory
- pgvector for semantic search (optional)

---

## Phase 4: Infrastructure - Week 4

### 4.1 Alembic Cleanup
- Merge migration heads
- Remove unused ENUMs
- Add missing indexes

### 4.2 Testing
- Integration tests: checkout → order → payment → notification
- Load tests for critical paths
- Contract tests for webhooks

---

## Dependencies to Add (pyproject.toml)
```toml
stripe = "^7.0"
sendgrid = "^6.10"
jinja2 = "^3.1"
celery = "^5.3"
redis = "^5.0"
boto3 = "^1.34"
langgraph = "^0.1"
langchain = "^0.2"
```

---

## Module Completion Checklist

| Module | Models | Schemas | Repositories | Services | Routes | Tests |
|--------|--------|---------|--------------|----------|--------|-------|
| payment | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| notification | ✅ | ✅ | ✅ | ☐ | ✅ | ☐ |
| order_automation | ✅ | ✅ | ✅ | ☐ | ✅ | ☐ |
| marketing_ai | ✅ | ✅ | ✅ | ☐ | ✅ | ☐ |
| admin | ✅ | ✅ | ✅ | ✅ | ✅ | ☐ |
| ai/agents | ✅ | ☐ | ☐ | ☐ | ☐ | ☐ |
| integrations | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| memory | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

---

## Execution Order
1. Payment (blocks checkout completion)
2. Notification delivery (blocks order confirmation)
3. Order automation (depends on 1,2)
4. Marketing AI (independent)
5. Admin RBAC (independent)
6. AI Agents (depends on integrations)
7. Integrations (parallel)
8. Memory (parallel)
9. Alembic + Tests (last)