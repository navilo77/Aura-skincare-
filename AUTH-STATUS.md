# AUTH-STATUS.md

<environment_details>
Current time: 2026-09-20T05:05:00-07:00
Working directory: D:\navil\TCH\auraskincare\.kilo\worktrees\1-5
Workspace root folder: D:\navil\TCH\auraskincare\.kilo\worktrees\1-5
</environment_details>

---

## Register

**Endpoint:** `POST /api/v1/auth/register`  
**Status:** PASS  
**Response:** 201 Created  
**Verified:** 2026-09-20

```json
{
    "email": "authphase@example.com",
    "full_name": "Auth Phase",
    "role": "customer",
    "is_active": true,
    "id": "070dc18d-9bad-4e94-a4af-d11e3d0f2c24",
    "is_verified": false,
    "created_at": "2026-09-20T04:57:55.834549",
    "updated_at": "2026-09-20T04:57:55.834549"
}
```

---

## Login

**Endpoint:** `POST /api/v1/auth/login`  
**Status:** PASS  
**Response:** 200 OK  
**Verified:** 2026-09-20

```json
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
}
```

**Issue:** Response does not include user identity. Client must decode JWT to obtain user ID.

**File:** `backend/app/modules/auth/routes/auth.py`  
**Line:** 46  
**Root Cause:** Endpoint returns `Token(access_token, refresh_token)` and discards the `user` object from `AuthService.login()`.

---

## Refresh

**Endpoint:** `POST /api/v1/auth/refresh`  
**Status:** PASS  
**Response:** 200 OK  
**Verified:** 2026-09-20

```json
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
}
```

---

## Logout

**Endpoint:** `POST /api/v1/auth/logout`  
**Status:** PASS  
**Response:** 204 No Content  
**Verified:** 2026-09-20

---

## /me

**Endpoint:** `GET /api/v1/auth/me?user_id={uuid}`  
**Status:** PASS (with caveat)  
**Response:** 200 OK  
**Verified:** 2026-09-20

```json
{
    "email": "authphase@example.com",
    "full_name": "Auth Phase",
    "role": "customer",
    "is_active": true,
    "id": "070dc18d-9bad-4e94-a4af-d11e3d0f2c24",
    "is_verified": false,
    "created_at": "2026-09-20T04:57:55.834549",
    "updated_at": "2026-09-20T05:02:42.002449"
}
```

**Issue:** Endpoint requires `user_id` as query parameter instead of extracting user from JWT. Calling without `user_id` returns 500 instead of 400.

**File:** `backend/app/modules/auth/routes/auth.py`  
**Line:** 80-88  
**Root Cause:** `get_me` is implemented as a public endpoint accepting raw `user_id` string, with no validation for empty input and no JWT integration.

---

## Verify Email

**Endpoint:** `POST /api/v1/auth/verify-email?token={token}`  
**Status:** PASS  
**Response:** 200 OK  
**Verified:** 2026-09-20

```json
{
    "message": "Email verified successfully"
}
```

**Flow verified end-to-end:**
1. `POST /api/v1/auth/resend-verification?email={email}` → creates `EmailVerification` record
2. `POST /api/v1/auth/verify-email?token={token}` → marks user as verified

**Database verified:** `users.is_verified` updated to `true`

---

## Resend Verification

**Endpoint:** `POST /api/v1/auth/resend-verification?email={email}`  
**Status:** PASS  
**Response:** 200 OK  
**Verified:** 2026-09-20

```json
{
    "message": "Verification email sent"
}
```

---

## Forgot Password

**Endpoint:** `POST /api/v1/auth/forgot-password`  
**Status:** FAIL — Not Found (404)  
**Verified:** 2026-09-20

**Root Cause:** Endpoint does not exist. No route, service, or model for forgot-password flow.

---

## Reset Password

**Endpoint:** `POST /api/v1/auth/reset-password`  
**Status:** FAIL — Not Found (404)  
**Verified:** 2026-09-20

**Root Cause:** Endpoint does not exist. No route, service, or model for reset-password flow.

---

## Summary

| Flow | Status |
|------|--------|
| Register | PASS |
| Login | PASS |
| Refresh | PASS |
| Logout | PASS |
| /me | PASS (misdesigned) |
| Verify Email | PASS |
| Resend Verification | PASS |
| Forgot Password | MISSING |
| Reset Password | MISSING |

---

## Outstanding Issues

1. **Login response missing user data** — client cannot determine user ID from response
2. **/me endpoint misdesigned** — requires client-supplied `user_id` instead of JWT extraction
3. **Forgot Password endpoint missing**
4. **Reset Password endpoint missing**
