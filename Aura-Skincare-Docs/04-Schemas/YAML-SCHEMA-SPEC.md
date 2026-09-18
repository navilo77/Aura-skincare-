# YAML Schema Specification

---

Document ID: SCH-000

Title: YAML Schema Specification

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Schema

Last Updated: 2026-09-15

---

# 1. Purpose

This document defines the official YAML standard used throughout the Aura Documentation System.

Every YAML document must follow these rules to ensure consistency, readability, machine validation, and AI compatibility.

---

# 2. Design Principles

- Documentation First
- Single Source of Truth (SSoT)
- Human Readable
- AI Readable
- Machine Validated
- Version Controlled
- Modular
- Reusable

---

# 3. File Naming

Use lowercase.

Words are separated using hyphen (-).

Examples

project.yaml

requirement.yaml

architecture.instance.yaml

customer-ai-agent.contract.yaml

---

# 4. Encoding

UTF-8

Indentation: 2 Spaces

Never use Tabs.

---

# 5. Required Top-Level Sections

Every YAML document should contain the following sections when applicable.

metadata

definition

references

validation

---

# 6. Metadata Standard

Every document must include metadata.

Example

metadata:

  id:

  title:

  version:

  status:

  owner:

  category:

  created:

  updated:

---

# 7. Status Values

Allowed values

Draft

Review

Approved

Deprecated

Archived

---

# 8. Versioning

Semantic Versioning

1.0

1.1

1.2

2.0

---

# 9. Naming Rules

IDs should be unique.

Examples

REQ-001

FEAT-005

API-003

RULE-010

ARCH-002

---

# 10. References

A document may reference other documents.

Example

references:

  requirements:

    - REQ-001

  features:

    - FEAT-002

---

# 11. Validation Rules

Every schema must define

Required Fields

Optional Fields

Allowed Values

Data Types

---

# 12. AI Compatibility

All YAML files must be

Predictable

Consistent

Structured

Self Describing

Machine Validated

---

# 13. Change Policy

Never delete existing fields.

Deprecate instead.

Maintain backward compatibility whenever possible.

---

# 14. Official Rule

All Aura YAML documents MUST follow this specification.