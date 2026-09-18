# Unit Testing

---

Document ID: TEST-002

Title: Unit Testing

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Testing

Last Updated: 2026-09-15

---

# Purpose

Defines standards for testing individual software units in isolation.

---

# Scope

Unit testing applies to:

- Business Logic
- API Services
- Utility Functions
- Database Helpers
- AI Utility Modules

---

# Principles

- Independent
- Repeatable
- Fast
- Automated
- Deterministic

---

# Coverage Goals

Target minimum coverage:

- Business Logic ≥ 90%
- Utility Functions ≥ 95%
- API Services ≥ 85%

---

# Test Cases

Verify:

- Expected output
- Invalid input
- Boundary values
- Error handling

---

# Execution

Run:

- Before every commit
- During CI
- Before release

---

# Related Documents

- testing-strategy.md
- integration-testing.md

---

# Core Principle

Every software unit should behave correctly under both normal and exceptional conditions.