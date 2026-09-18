17-Automation/n8n-workflows.md
````markdown
# n8n Workflows

---

Document ID: AUTO-007

Title: n8n Workflows

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Automation

Last Updated: 2026-09-15

---

# Purpose

Defines standards, architecture, governance, and best practices for all n8n workflows used within the Aura platform.

The objective is to ensure every workflow is secure, maintainable, observable, reusable, and production-ready.

---

# Scope

n8n is responsible for orchestrating automation between internal services and external integrations.

Examples include:

- AI Automation
- Order Automation
- Customer Communication
- Payment Processing
- Marketing Automation
- Scheduled Jobs
- Administrative Automation

---

# Workflow Categories

## Customer

- Customer Onboarding
- Customer Follow-up
- Loyalty Automation
- Review Request

---

## Commerce

- Order Processing
- Payment Verification
- Refund Processing
- Inventory Synchronization

---

## AI

- AI Recommendation
- Prompt Processing
- AI Evaluation
- Knowledge Synchronization

---

## Communication

- Email Automation
- WhatsApp Automation
- Messenger Automation
- Instagram Automation

---

## Operations

- Backup Automation
- Monitoring Alerts
- Report Generation
- Scheduled Maintenance

---

# Workflow Architecture

Trigger

↓

Input Validation

↓

Business Rules

↓

Service/API Calls

↓

AI Processing (Optional)

↓

Output Validation

↓

Notification

↓

Logging

↓

Completion

---

# Trigger Types

Supported triggers:

- Webhook
- Schedule (Cron)
- Manual
- API Trigger
- Event Trigger
- Queue Trigger

---

# Naming Convention

Use descriptive names.

Examples:

- Customer_Onboarding
- Order_Confirmation
- Payment_Verification
- AI_Product_Recommendation
- Daily_Sales_Report

---

# Folder Organization

Production

Development

Testing

Archived

Experimental

---

# Credentials Management

Credentials must never be hardcoded.

Use:

- Environment Variables
- n8n Credential Manager
- External Secret Manager (Future)

Supported credentials:

- OpenAI
- Gemini
- Supabase (Managed PostgreSQL)
- Redis
- Email Provider
- WhatsApp API
- Meta API
- Payment Gateway

---

# Error Handling

Every workflow must:

- Validate inputs
- Catch failures
- Log errors
- Retry recoverable failures
- Escalate critical failures

---

# Retry Strategy

Recoverable errors:

- Network Failure
- Timeout
- Rate Limit
- Temporary Service Failure

Maximum retries should follow the Retry Policy.

---

# Logging

Log:

- Workflow ID
- Execution Time
- Trigger
- User (if applicable)
- Status
- Duration
- Errors

Sensitive information must never be logged.

---

# Monitoring

Monitor:

- Success Rate
- Failure Rate
- Retry Count
- Average Duration
- Queue Size
- AI Response Time

---

# Security

- HTTPS only
- Verify Webhooks
- Validate Inputs
- Protect Credentials
- Apply RBAC
- Audit Executions

---

# Version Control

Every workflow must include:

- Version Number
- Owner
- Last Updated
- Change History

Production workflows require review before deployment.

---

# Deployment

Deployment process:

Development

↓

Testing

↓

Staging

↓

Production

Rollback must be available for every workflow release.

---

# Best Practices

- One workflow = One business process.
- Reuse sub-workflows where possible.
- Avoid duplicated logic.
- Keep workflows modular.
- Validate every external response.
- Design for idempotency.
- Document every workflow.

---

# Related Documents

- automation-overview.md
- workflow-standards.md
- retry-policy.md
- failure-handling.md
- webhook-policy.md

---

# Core Principle

Every n8n workflow must be secure, reusable, observable, version-controlled, and aligned with Aura's enterprise automation standards.