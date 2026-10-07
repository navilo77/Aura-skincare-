# CUSTOMER-004 — Customer Module Services

## Status: PASSED

---

## Files Changed

- `backend/app/modules/customer/services/__init__.py` — Exports CustomerService
- `backend/app/modules/customer/services/customer.py` — CustomerService implementation

---

## Services Implemented

### CustomerService

#### Methods
- `create(full_name, email, phone, status, skin_type, skin_concerns)` — Create new customer with validation
- `update(customer_id, ...)` — Update existing customer with validation
- `delete(customer_id)` — Soft delete customer
- `get_by_id(customer_id)` — Get customer by ID
- `get_list(skip, limit, status, search)` — List customers with pagination, filtering, search

#### Business Rules
1. Email uniqueness enforced before persistence
2. Phone uniqueness enforced before persistence (if provided)
3. Email normalization: lowercase, trimmed
4. Phone normalization: trimmed
5. Full name normalization: trimmed
6. Status validation: must be one of active, inactive, suspended
7. Soft delete only via repository
8. Duplicate prevention via existence checks
9. Input validation before any database operation

#### Validation
- [x] Business rules implemented
- [x] No SQLAlchemy in routes (service layer abstracts DB)
- [x] Repository abstraction respected
- [x] Imports successful
- [x] ruff check passed
- [x] mypy reviewed (pre-existing forward-reference and UUID generic-type issues)

---

## Issues

Pre-existing mypy issues consistent with Order/Product modules:
- Forward reference type annotations in models
- UUID generic type arguments

---

## Recommendation

Proceed to CUSTOMER-005 (Schemas).
