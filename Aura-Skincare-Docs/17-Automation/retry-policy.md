# Retry Policy

---

Document ID: AUTO-005

Title: Retry Policy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Automation

Last Updated: 2026-09-15

---

# Purpose

Defines retry strategies for failed automation workflows, background jobs, and external integrations.

---

# Retry Objectives

- Recover from temporary failures.
- Reduce manual intervention.
- Improve workflow reliability.
- Prevent duplicate processing.

---

# Retry Strategy

Retry only for:

- Temporary network failures
- Service unavailable
- Timeout
- Rate limiting

Do Not Retry:

- Invalid request
- Authentication failure
- Authorization failure
- Business validation failure

---

# Retry Schedule

Attempt 1

↓

Wait 30 Seconds

↓

Attempt 2

↓

Wait 2 Minutes

↓

Attempt 3

↓

Escalate Failure

---

# Retry Rules

- Use exponential backoff where appropriate.
- Limit maximum retry attempts.
- Log every retry.
- Prevent duplicate business actions.

---

# Monitoring

Track:

- Retry Count
- Success After Retry
- Permanent Failure
- Average Recovery Time

---

# Related Documents

- workflow-standards.md
- failure-handling.md
- webhook-policy.md

---

# Core Principle

Retry only recoverable failures and never compromise data integrity or business consistency.