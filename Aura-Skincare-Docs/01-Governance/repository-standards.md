98-Governance/repository-standards.md
````markdown
# Repository Standards

---

Document ID: GOV-007

Title: Repository Standards

Version: 1.0.0

Status: Approved

Owner: Aura Skincare

Category: Governance

Last Updated: 2026-09-16

---

# Purpose

Defines the mandatory repository structure, documentation standards, naming conventions, and governance rules for the Aura Documentation Repository.

---

# Objectives

- Maintain a consistent repository structure.
- Standardize documentation across all domains.
- Improve collaboration between Product, Engineering, QA, AI, and Operations.
- Support AI-assisted development.
- Enable long-term maintainability.

---

# Repository Structure

The repository is organized into numbered sections.

Example:

00-Foundation/

01-Research/

02-Requirements/

...

18-Analytics/

19-Testing/

98-Governance/

99-Templates/

Every document must belong to exactly one section.

---

# Naming Standards

## Folder Names

Format:

NN-Section-Name

Examples:

00-Foundation

05-PRD

06-SAD

18-Analytics

99-Templates

---

## File Names

Rules:

- Lowercase
- Hyphen-separated
- Descriptive
- Markdown (.md) or YAML (.yaml)

Examples:

product-catalog.md

api-testing.md

feature.template.yaml

---

# Document Metadata

Every document should include:

- Document ID
- Title
- Version
- Status
- Owner
- Category
- Last Updated

---

# Document IDs

Each document type uses a unique prefix.

| Prefix | Category |
|---------|----------|
| PRD | Product Requirements |
| SAD | Software Architecture |
| API | API Specifications |
| REQ | Requirements |
| NFR | Non-Functional Requirements |
| ADR | Architecture Decisions |
| AI | Artificial Intelligence |
| SEC | Security |
| INT | Integrations |
| AUTO | Automation |
| ANA | Analytics |
| TEST | Testing |
| GOV | Governance |

Document IDs must be unique within the repository.

---

# Versioning

Documentation follows Semantic Versioning.

MAJOR.MINOR.PATCH

Examples:

- 1.0.0
- 1.1.0
- 1.1.1
- 2.0.0

Refer to:

GOV-004 Versioning Policy

---

# Cross References

Related documents should be referenced explicitly.

Example:

Related Documents

- API-001
- PRD-003
- SAD-002

Broken references should not exist.

---

# Templates

All new documents must be created from the approved templates in:

99-Templates/

Templates must not be edited directly.

---

# Repository Rules

- Keep one source of truth.
- Avoid duplicate documentation.
- Archive deprecated documents.
- Review before approval.
- Maintain consistent formatting.
- Preserve document history.
- Update related documents when changes occur.

---

# Quality Checklist

Every document should be:

- Accurate
- Complete
- Consistent
- Traceable
- Reviewable
- Versioned
- Approved

---

# Repository Lifecycle

New Document

↓

Draft

↓

Review

↓

Approved

↓

Frozen

↓

Deprecated

↓

Archived

---

# Exceptions

Any exception to these standards must:

- Be documented.
- Be approved.
- Include a business justification.

---

# Related Documents

- GOV-001 Documentation Policy
- GOV-002 Document Lifecycle
- GOV-003 Review Process
- GOV-004 Versioning Policy
- GOV-005 Change Management
- GOV-006 Ownership Matrix
- 99-Templates/

---

# Core Principle

The repository is the single source of truth for the Aura platform. Every document must follow standardized structure, governance, and lifecycle rules to ensure consistency, traceability, and long-term maintainability.