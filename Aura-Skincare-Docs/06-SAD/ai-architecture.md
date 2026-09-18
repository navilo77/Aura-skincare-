
# AI Architecture

---

Document ID: SAD-010

Title: AI Architecture

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: AI Architecture

Last Updated: 2026-09-15

---

# AI Architecture Overview

```text
Customer
      │
      ▼
Router AI Agent
      │
 ┌────┼───────────────┐
 ▼    ▼       ▼       ▼
Customer  Admin  Marketing  Development
AI Agent AI Agent AI Agent AI Agent
```

---

# AI Agents

## Router AI Agent

Responsibilities

- Intent detection
- Request routing
- Session management
- Context forwarding

---

## Customer AI Agent

Responsibilities

- Skincare consultation
- Product recommendation
- Customer support

---

## Admin AI Agent

Responsibilities

- Product management
- Inventory insights
- Reporting assistance

---

## Marketing AI Agent

Responsibilities

- Campaign generation
- Content creation
- Customer segmentation

---

## Development AI Agent

Responsibilities

- Code generation
- Documentation
- Architecture validation
- API design
- Test generation

---

# Shared Services

- Prompt Library
- Business Rules
- Product Knowledge
- Conversation Memory
- Analytics

---

# LLM Provider

Primary

- OpenAI

Future

- Anthropic
- Google Gemini
- Local Models

---

# Core Principle

Each AI agent has a single responsibility and collaborates through the Router Agent.