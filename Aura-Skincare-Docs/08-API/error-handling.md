# API Error Handling

---

Document ID: API-DOC-002

Title: API Error Handling

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: API

Last Updated: 2026-09-15

---

# Purpose

Defines the standard error response format.

---

# Response Format

```json
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product not found."
  }
}
```

---

# HTTP Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error

---

# Rules

- Always return JSON.
- Never expose stack traces.
- Error codes must remain stable.

---

# Core Principle

Errors must be predictable, secure, and easy to debug.