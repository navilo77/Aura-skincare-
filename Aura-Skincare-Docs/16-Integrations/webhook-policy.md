# Webhook Policy

---

Document ID: INT-008

Title: Webhook Policy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Integrations

Last Updated: 2026-09-15

---

# Purpose

Defines standards for receiving, validating, and processing webhook events from external providers.

---

# Supported Sources

- Payment Gateway
- WhatsApp
- Messenger
- Instagram
- Courier
- Future Integrations

---

# Webhook Workflow

Receive Request

↓

Verify Signature

↓

Validate Payload

↓

Prevent Duplicate Processing

↓

Execute Business Logic

↓

Return Response

↓

Log Event

---

# Validation Rules

- Verify webhook signature.
- Reject invalid requests.
- Prevent replay attacks.
- Ensure idempotent processing.

---

# Retry Policy

- Retry transient failures.
- Log all retry attempts.
- Alert after repeated failures.

---

# Security

- HTTPS Only
- Signature Verification
- Timestamp Validation
- IP Allowlisting (where supported)

---

# Core Principle

Every webhook must be authenticated, validated, and processed exactly once.