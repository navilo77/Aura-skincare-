16-Integrations/payment.md
````markdown
# Payment Integration

---

Document ID: INT-007

Title: Payment Integration

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Integrations

Last Updated: 2026-09-15

---

# Purpose

Defines standards for integrating payment providers with the Aura platform.

---

# Supported Providers

## Bangladesh

- SSLCommerz
- bKash (Future)
- Nagad (Future)

---

## International

- Stripe
- PayPal (Future)

---

# Payment Workflow

Customer Checkout

↓

Create Payment Request

↓

Redirect to Gateway

↓

Gateway Processing

↓

Payment Verification

↓

Update Order Status

↓

Send Confirmation

---

# Payment Status

- Pending
- Successful
- Failed
- Cancelled
- Refunded

---

# Validation Rules

- Verify every callback.
- Prevent duplicate payments.
- Match payment with order.
- Record transaction reference.

---

# Security

- HTTPS Required
- Signed Webhooks
- Audit Logging
- Server-side Verification

---

# Related Documents

- webhook-policy.md
- audit-logging.md
- authentication-policy.md

---

# Core Principle

A payment is considered valid only after successful server-side verification.