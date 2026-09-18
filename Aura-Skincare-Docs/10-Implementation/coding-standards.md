# Coding Standards

---

Document ID: IMP-001

Title: Coding Standards

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Implementation

Last Updated: 2026-09-15

---

# Purpose

Defines the coding standards for all Aura platform development.

---

# General Principles

- Write clean and readable code.
- Prefer simplicity over complexity.
- Avoid duplicated logic (DRY).
- Follow SOLID principles where applicable.
- Keep functions focused on a single responsibility.

---

# Naming Conventions

## Variables

Use descriptive `snake_case` or `camelCase` according to the language standard.

Examples:

- customerId
- productName
- orderTotal

---

## Functions

Use verb-based names.

Examples:

- createOrder()
- calculateTotal()
- recommendProducts()

---

## Classes

Use PascalCase.

Examples:

- CustomerService
- ProductRepository
- RecommendationEngine

---

## Constants

Use UPPER_SNAKE_CASE.

Examples:

- MAX_CART_ITEMS
- DEFAULT_PAGE_SIZE

---

# Error Handling

- Handle expected errors gracefully.
- Never expose internal stack traces.
- Log errors with sufficient context.

---

# Documentation

- Public functions should include comments or docstrings.
- Complex business logic must be documented.

---

# Security

- Never hardcode secrets.
- Always validate input.
- Use parameterized database queries.

---

# AI Development Rules

- Do not hardcode prompts in business logic.
- Read prompts from managed prompt configuration.
- AI responses must pass business-rule validation before being returned.

---

# Core Principle

Readable, secure, and maintainable code is more valuable than clever code.