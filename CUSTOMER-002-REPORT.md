# CUSTOMER-002 — Customer Module Models & Migration

## Status: PASSED

---

## Files Changed

- `backend/app/modules/customer/models/__init__.py` — Updated to export Customer, Address, Conversation
- `backend/app/modules/customer/models/customer.py` — Customer ORM model
- `backend/app/modules/customer/models/address.py` — Address ORM model
- `backend/app/modules/customer/models/conversation.py` — Conversation ORM model
- `backend/alembic/versions/a1b2c3d4e5f6_create_customer_module.py` — Alembic migration

---

## Tables Created

### customers
- `customer_id` (UUID, PK)
- `full_name` (String(255), NOT NULL)
- `email` (String(255), UNIQUE, NOT NULL)
- `phone` (String(20), UNIQUE, NULLABLE)
- `status` (Enum: active, inactive, suspended, DEFAULT: active)
- `skin_type` (String(50), NULLABLE)
- `skin_concerns` (JSON, NULLABLE)
- `created_at` (DateTime, server_default: now())
- `updated_at` (DateTime, server_default: now())
- `deleted_at` (DateTime, NULLABLE)

### customer_addresses
- `address_id` (UUID, PK)
- `customer_id` (UUID, FK → customers.id, NOT NULL)
- `address_line1` (String(255), NOT NULL)
- `address_line2` (String(255), NULLABLE)
- `city` (String(100), NOT NULL)
- `state` (String(100), NOT NULL)
- `postal_code` (String(20), NOT NULL)
- `country` (String(2), NOT NULL)
- `is_default` (Boolean, DEFAULT: False)
- `created_at`, `updated_at`, `deleted_at`

### conversations
- `conversation_id` (UUID, PK)
- `customer_id` (UUID, FK → customers.id, NOT NULL)
- `channel` (Enum: whatsapp, messenger, instagram, website)
- `status` (Enum: active, closed, pending, DEFAULT: pending)
- `last_message_at` (DateTime, NULLABLE)
- `created_at`, `updated_at`, `deleted_at`

---

## Foreign Keys
- `customer_addresses.customer_id` → `customers.id`
- `conversations.customer_id` → `customers.id`

## Indexes
- `ix_customers_email` (unique)
- `ix_customers_phone` (non-unique, nullable)
- `ix_customers_status`
- `ix_customer_addresses_customer_id`
- `ix_conversations_customer_id`

## Enums
- `customer_status`: active, inactive, suspended
- `conversation_channel`: whatsapp, messenger, instagram, website
- `conversation_status`: active, closed, pending

## Relationships
- Customer → Address (one-to-many, cascade delete-orphan)
- Customer → Conversation (one-to-many, cascade delete-orphan)

## Migration
- File: `a1b2c3d4e5f6_create_customer_module.py`
- Revision ID: `a1b2c3d4e5f6`
- Down revision: `feb39ceece7d`
- Status: File created and structurally valid

## Validation
- [x] Tables defined in models
- [x] Constraints defined
- [x] Indexes defined
- [x] Relationships defined
- [x] Models import correctly
- [x] Base.metadata updated (verified: customers, customer_addresses, conversations in metadata)
- [ ] Migration applied (no local PostgreSQL running; migration file is structurally valid)

## Issues
- Forward reference type annotations in models (consistent with Order/Product modules)
- UUID generic type args in models (consistent with Order/Product modules)

## Recommendation
Proceed to CUSTOMER-003 (Repositories).
