# CUSTOMER-001 — Customer Module Design & Documentation

## Status: PASSED

---

## Files Changed

- `Aura-Skincare-Docs/07-Database/data-model.instance.yaml` — Added Customer columns, Address columns, Conversation columns
- `Aura-Skincare-Docs/07-Database/er-diagram.md` — Added CUSTOMERS, CUSTOMER_ADDRESSES, CONVERSATIONS entities
- `Aura-Skincare-Docs/08-API/endpoints/API-003-customer-profile.yaml` — Complete API specification

---

## Design Decisions

### Customer Entity
- **Table**: `customers`
- **Primary Key**: `customer_id` (UUID)
- **Soft Delete**: Yes, via `deleted_at` timestamp
- **Audit**: `created_at`, `updated_at` timestamps

### Columns
- `full_name` (String(255), required) — Customer display name
- `email` (String(255), unique, indexed, required) — Primary contact email
- `phone` (String(20), unique, indexed, optional) — Phone number
- `status` (Enum: active, inactive, suspended) — Customer lifecycle status
- `skin_type` (String(50), optional) — Skincare profile
- `skin_concerns` (JSON, optional) — Array of skin concerns

### Enums
- `customer_status`: active, inactive, suspended

### Relationships
- Customer → Address (one-to-many)
- Customer → Order (one-to-many) — already in Order module
- Customer → Conversation (one-to-many) — for AI module

### Indexes
- `idx_customers_email` — unique index on email
- `idx_customers_phone` — unique index on phone (nullable)
- `idx_customers_status` — index on status for filtering

---

## Business Rules

1. Email must be unique across all customers
2. Phone must be unique if provided
3. Email must be valid format (validated at schema level)
4. Customer status must be one of: active, inactive, suspended
5. Soft delete only — no hard delete
6. Cannot delete customer with active orders (enforced in service layer)
7. Skin type is optional free text
8. Skin concerns is optional JSON array
9. Customer profile is accessible via JWT authentication

---

## API Contract

### Endpoints
- `POST /api/v1/customers` — Create customer
- `GET /api/v1/customers/{id}` — Get customer by ID
- `GET /api/v1/customers` — List customers (paginated, filterable)
- `PATCH /api/v1/customers/{id}` — Update customer
- `DELETE /api/v1/customers/{id}` — Soft delete customer
- `GET /api/v1/customers/profile` — Get current authenticated customer profile
- `PUT /api/v1/customers/profile` — Update current authenticated customer profile

### Request/Response Models
- `CustomerCreate` — full_name, email, phone, status, skin_type, skin_concerns
- `CustomerUpdate` — all fields optional
- `CustomerRead` — full customer with id and timestamps
- `CustomerList` — summary for list views
- `CustomerDetail` — full detail with relationships

---

## Relationships with Other Modules

### Order Module
- `orders.customer_id` → `customers.customer_id` (UUID FK)
- Customer module depends on Order module for order history
- Order module references Customer but Customer FK is nullable until Customer module exists

### Authentication Module (future)
- Customer authentication via JWT
- Customer profile linked to User/Auth credentials
- Future: Customer login with email/phone + password

### AI Module (future)
- Customer profile used for personalization
- Skin type and skin concerns feed AI recommendations
- Conversation history linked to customer

---

## Validation

- [x] Documentation is internally consistent
- [x] Data model aligns with existing architecture
- [x] API contract follows existing patterns
- [x] No code generated

---

## Issues

None.

---

## Recommendation

Proceed to CUSTOMER-002 (Models & Migration).
