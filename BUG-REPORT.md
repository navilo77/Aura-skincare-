# BUG-REPORT.md

<environment_details>
Current time: 2026-09-20T04:40:00-07:00
Working directory: D:\navil\TCH\auraskincare\.kilo\worktrees\1-5
Workspace root folder: D:\navil\TCH\auraskincare\.kilo\worktrees\1-5
</environment_details>

---

## Executive Summary

End-to-end verification was performed on the Aura Skincare application. The backend API was started and tested against live HTTP endpoints. The application **cannot be considered feature-complete or production-ready** due to critical bugs, missing features, and infrastructure issues.

**Verdict: BLOCKED — Multiple critical bugs prevent full user flow verification.**

---

## Verification Environment

- **Backend:** Started via `uvicorn app.main:app` on `http://localhost:8000`
- **Database:** SQLite (`test.db`) — tables created via `Base.metadata.create_all`
- **Frontend:** Not started (backend blockers prevented frontend testing)
- **Browser:** Not tested (frontend not started)

---

## Authentication Flow Bugs

### BUG-AUTH-001: Login Response Missing User Identity

**Step:** Call `POST /api/v1/auth/login` with valid credentials

**Expected:** Response includes user ID, email, role, and tokens

**Actual:**
```json
{
    "access_token": "...",
    "refresh_token": "...",
    "token_type": "bearer"
}
```

**Root Cause:** The login endpoint returns only `Token(access_token, refresh_token)` and discards the `user` object returned by `AuthService.login()`.

**File:** `backend/app/modules/auth/routes/auth.py`
**Line:** 46
**Fix:** Return a response model that includes user data, or include user fields in the Token schema.

---

### BUG-AUTH-002: `/me` Endpoint Crashes on Empty `user_id`

**Step:** Call `GET /api/v1/auth/me?user_id=` with empty user_id

**Expected:** 400 Bad Request with validation error

**Actual:** 500 Internal Server Error
```
ValueError: badly formed hexadecimal UUID string
```

**Root Cause:** The endpoint accepts `user_id` as a raw `str` and passes it directly to `uuid.UUID()` without validating that it is non-empty.

**File:** `backend/app/modules/auth/routes/auth.py`
**Line:** 83
**Fix:** Add validation that `user_id` is not empty before converting to UUID, or use a proper UUID type in the query parameter.

---

### BUG-AUTH-003: `/me` Endpoint Requires Client-Supplied `user_id`

**Step:** Call `GET /api/v1/auth/me` without `user_id` query parameter

**Expected:** Endpoint extracts user ID from JWT token and returns current user

**Actual:** 422 Unprocessable Content (missing required query parameter)

**Root Cause:** The `/me` endpoint is implemented as a public endpoint requiring `user_id` as a query parameter instead of using the authenticated user from the JWT token. This is a security anti-pattern and breaks standard auth flow.

**File:** `backend/app/modules/auth/routes/auth.py`
**Line:** 80-88
**Fix:** Refactor `/me` to use `get_current_user` dependency and remove `user_id` parameter.

---

### BUG-AUTH-004: Missing Forgot Password / Reset Password Endpoints

**Step:** Call password reset flow (`POST /api/v1/auth/forgot-password`, `POST /api/v1/auth/reset-password`)

**Expected:** Endpoints exist and handle password reset

**Actual:** 404 Not Found — endpoints do not exist

**Root Cause:** The auth module does not implement forgot password or reset password functionality. No routes, services, or models exist for password reset tokens in the auth flow.

**File:** `backend/app/modules/auth/routes/` (missing files)
**Fix:** Implement forgot password and reset password endpoints with token generation and validation.

---

### BUG-AUTH-005: Email Verification Token Not Created on Registration

**Step:** Register a new user and check for `EmailVerification` record

**Expected:** `EmailVerification` record is created with a token

**Actual:** No `EmailVerification` record is created. The `verify-email` endpoint is useless because there is no token to verify.

**Root Cause:** `AuthService.register()` does not create an `EmailVerification` record. The email verification flow is incomplete.

**File:** `backend/app/modules/auth/services/auth.py`
**Line:** 19-33
**Fix:** Create `EmailVerification` record in `register()` with a secure token.

---

## AI Module Bugs

### BUG-AI-001: AI Router Prefix Duplication

**Step:** Call `POST /api/v1/ai/chat`

**Expected:** 200 OK

**Actual:** 404 Not Found

**Root Cause:** The AI router is defined with `prefix="/ai"` and then included in the v1 router also with `prefix="/ai"`, resulting in duplicated path `/api/v1/ai/ai/chat`.

**File:** `backend/app/modules/ai/routes/ai.py` (line 7) and `backend/app/api/v1/__init__.py` (line 39)
**Fix:** Remove the `prefix="/ai"` from either the router definition or the `include_router` call.

---

### BUG-AI-002: AI Tables Missing from Database

**Step:** Call `POST /api/v1/ai/ai/chat` (correct path)

**Expected:** 200 OK or 401/422 depending on auth

**Actual:** 500 Internal Server Error
```
sqlite3.OperationalError: no such table: ai_conversations
```

**Root Cause:** The `ai`, `marketing_ai`, and `order_automation` module directories are missing `__init__.py` files, making them namespace packages. `pkgutil.walk_packages` fails to discover their submodules, so `Base.metadata.create_all` does not register their models.

**File:** `backend/app/modules/ai/__init__.py` (missing), `backend/app/modules/marketing_ai/__init__.py` (missing), `backend/app/modules/order_automation/__init__.py` (missing)
**Fix:** Add empty `__init__.py` files to `app/modules/ai/`, `app/modules/marketing_ai/`, and `app/modules/order_automation/`.

---

## Infrastructure Bugs

### BUG-INFRA-001: Multiple Alembic Migration Heads

**Step:** Run `alembic upgrade head`

**Expected:** All migrations apply cleanly

**Actual:**
```
FAILED: Multiple head revisions are present for given argument 'head'
```

**Root Cause:** Migration history has branched into 4 independent heads:
- `28a4f978cc5d`
- `a1b2c3d4e5f6`
- `d5e6f7a8b9c0`
- `f6a7b8c9d0e1`

**File:** `backend/alembic/versions/*.py`
**Fix:** Create an Alembic merge migration to consolidate heads into a single linear chain.

---

### BUG-INFRA-002: SQLite Migration Incompatibility

**Step:** Run `alembic upgrade heads`

**Expected:** All tables created

**Actual:**
```
NotImplementedError: No support for ALTER of constraints in SQLite dialect
```

**Root Cause:** Migration `41e2eb274d18_add_product_foreign_keys.py` uses `op.create_foreign_key()` which is not supported by SQLite's ALTER TABLE.

**File:** `backend/alembic/versions/41e2eb274d18_add_product_foreign_keys.py`
**Line:** 33
**Fix:** Use `op.batch_alter_table()` for SQLite or use PostgreSQL for all environments.

---

### BUG-INFRA-003: Missing `.env` File

**Step:** Start backend server

**Expected:** Server loads configuration from `.env`

**Actual:** No `.env` file exists; server starts with default/environment variables only

**Root Cause:** `backend/.env` does not exist. Only `backend/.env.example` is present.

**File:** `backend/.env` (missing)
**Fix:** Copy `backend/.env.example` to `backend/.env` and fill in real values.

---

## Missing Module `__init__.py` Files

### BUG-INFRA-004: Namespace Packages Break Table Creation

**Step:** Run `Base.metadata.create_all`

**Expected:** All tables created

**Actual:** Tables for `ai`, `marketing_ai`, and `order_automation` modules are missing

**Root Cause:** The following module directories lack `__init__.py`:
- `backend/app/modules/ai/`
- `backend/app/modules/marketing_ai/`
- `backend/app/modules/order_automation/`

**File:** Multiple (see above paths)
**Fix:** Add empty `__init__.py` files to each directory.

---

## Lint/Code Quality Issues

### BUG-LINT-001: 259 Ruff Lint Errors

**Step:** Run `ruff check .`

**Expected:** 0 errors

**Actual:** 259 errors

**Categories:**
- E501 Line too long (>88 chars): ~120 instances
- I001 Import sorting: ~60 instances
- F401 Unused imports: ~40 instances
- F811 Redefinitions: ~10 instances
- UP031 Percent format: ~2 instances

**Files with most issues:**
- `backend/app/modules/order_automation/repositories/automation.py`
- `backend/app/modules/order_automation/routes/automation.py`
- `backend/app/modules/order_automation/services/automation.py`
- `backend/app/modules/order_automation/tasks/automation_tasks.py`
- `backend/app/modules/marketing_ai/routes/marketing.py`
- `backend/app/modules/marketing_ai/services/marketing.py`
- `backend/app/modules/product/routes/*.py`
- `backend/app/shared/database/base.py`
- `backend/app/shared/database/session.py`

**Fix:** Run `ruff check --fix` and manually fix remaining line-length issues.

---

## Missing Features

### BUG-FEAT-001: No Forgot Password / Reset Password

**Impact:** Users cannot reset forgotten passwords

**Affected Flow:** Authentication

---

### BUG-FEAT-002: Email Verification Not Wired to Registration

**Impact:** Users never receive verification emails; `verify-email` endpoint is non-functional

**Affected Flow:** Authentication

---

### BUG-FEAT-003: No Search/Filter Query Parameters on Product List

**Step:** Call `GET /api/v1/products?search=...&category_id=...&brand_id=...`

**Expected:** Filtered results

**Actual:** Returns all products (no filtering implemented)

**Root Cause:** Product list endpoint does not accept or process search/filter query parameters.

**File:** `backend/app/modules/product/routes/product.py`
**Fix:** Add query parameter handling for search, category, brand, price range, etc.

---

## Admin Flow Status

**Tested:**
- Product creation: Partial — requires `slug` and `sku` fields (schema enforces this correctly)
- Product listing: Works (returns empty list when no products exist)
- Admin dashboard: Not tested (requires admin user and data)

**Blocked:**
- All admin flows blocked by missing data seeding and authentication issues

---

## Customer Flow Status

**Tested:**
- Registration: ✅ Works
- Login: ✅ Works
- Refresh token: ✅ Works
- Logout: ✅ Works
- Product listing: ✅ Works (empty)
- `/me` endpoint: ⚠️ Works only with explicit `user_id` query param

**Blocked:**
- Cart, wishlist, checkout, orders — blocked by missing product/category/brand data
- Profile, address CRUD — not tested due to time constraints

---

## Order Automation Flow Status

**Tested:**
- None — blocked by missing `__init__.py` causing missing database tables

**Root Cause:** Missing `app/modules/order_automation/__init__.py`

---

## Marketing AI Flow Status

**Tested:**
- None — blocked by missing `__init__.py` causing missing database tables

**Root Cause:** Missing `app/modules/marketing_ai/__init__.py`

---

## Summary

| Category | Count | Severity |
|----------|-------|----------|
| Critical Bugs | 5 | Blocker |
| Missing Features | 3 | High |
| Infrastructure | 4 | Blocker |
| Lint Issues | 259 | Medium |
| Total Issues | 271 | — |

---

## Recommended Fix Order

1. **BUG-INFRA-004:** Add missing `__init__.py` files to `ai`, `marketing_ai`, `order_automation`
2. **BUG-INFRA-001:** Merge Alembic migration heads
3. **BUG-INFRA-002:** Fix SQLite migration compatibility
4. **BUG-INFRA-003:** Create `.env` file
5. **BUG-AUTH-001:** Include user data in login response
6. **BUG-AUTH-003:** Fix `/me` endpoint to use JWT
7. **BUG-AUTH-002:** Add validation to `/me` endpoint
8. **BUG-AUTH-004:** Implement forgot/reset password
9. **BUG-AUTH-005:** Wire email verification to registration
10. **BUG-AI-001:** Fix AI router prefix duplication
11. **BUG-LINT-001:** Fix lint issues
12. **BUG-FEAT-003:** Add search/filter to product list
