# Branching Strategy

---

Document ID: IMP-004

Title: Branching Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Implementation

Last Updated: 2026-09-15

---

# Purpose

Defines the Git branching workflow.

---

# Main Branches

- main → Production-ready code
- develop → Active development

---

# Feature Branches

Naming Convention:

```
feature/<feature-name>
```

Example:

```
feature/product-recommendation
```

---

# Bug Fix Branches

```
fix/<issue-name>
```

---

# Hotfix Branches

```
hotfix/<issue-name>
```

---

# Merge Rules

- Pull Request required.
- Code Review required.
- CI must pass before merge.

---

# Core Principle

Every change must be traceable, reviewed, and tested.