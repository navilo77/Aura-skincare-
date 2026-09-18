16-Integrations/email.md
````markdown
# Email Integration

---

Document ID: INT-004

Title: Email Integration

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Integrations

Last Updated: 2026-09-15

---

# Purpose

Defines standards for sending transactional and marketing emails.

---

# Supported Providers

Primary

- SMTP

Future

- Resend
- SendGrid
- Brevo
- Amazon SES

---

# Email Categories

## Transactional

- Account Verification
- Password Reset
- Order Confirmation
- Payment Confirmation
- Shipping Update

---

## Marketing

- Promotions
- Product Launches
- Newsletters
- Personalized Campaigns

---

# Delivery Rules

- Retry failed deliveries.
- Track delivery status.
- Record bounce events.
- Record unsubscribe requests.

---

# Security

- SPF
- DKIM
- DMARC
- TLS Required

---

# Related Documents

- analytics.md
- audit-logging.md

---

# Core Principle

Every email must be secure, traceable, and relevant to the customer.