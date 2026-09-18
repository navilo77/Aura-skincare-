# AI Providers

---

Document ID: INT-001

Title: AI Providers

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Integrations

Last Updated: 2026-09-15

---

# Purpose

Defines the AI providers supported by the Aura platform and the standards for selecting, configuring, and using them.

---

# Supported Providers

## Primary

- OpenAI

## Secondary

- Google Gemini

## Future

- Anthropic Claude
- Local LLM
- Azure OpenAI

---

# AI Capabilities

- Product Recommendation
- Customer Support
- Marketing Content
- Documentation Assistance
- Internal Development Support

---

# Provider Selection

Primary provider handles normal requests.

Secondary provider is used when:

- Primary provider is unavailable
- Failover is triggered
- Business rules require a different model

---

# Configuration

- API Keys stored securely
- Environment-based configuration
- Version controlled configuration

---

# Security

- HTTPS/TLS required
- Secrets stored outside source code
- Request and response logging
- Output validation before customer response

---

# Related Documents

- prompt-library.md
- router-logic.md
- prompt-security.md

---

# Core Principle

AI providers are replaceable implementation components behind a single business interface.