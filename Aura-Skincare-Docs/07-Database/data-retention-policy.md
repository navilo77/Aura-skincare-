# Data Retention Policy

---

Document ID: DB-011

Title: Data Retention Policy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines how long different categories of data are retained on the Supabase platform.

---

# Retention Schedule

| Data Type | Retention |
|------------|-----------|
| Orders | 7 Years |
| Payments | 7 Years |
| Audit Logs | 7 Years |
| Customer Profiles | Until Account Deletion + Legal Requirements |
| AI Conversations | 2 Years |
| Event Logs | 1 Year |
| Temporary Data | 30 Days |
| Backups | 90 Days (managed by Supabase) |

---

# Deletion Rules

- Expired data must be securely deleted.
- Deletion must be logged.
- Legal hold overrides automatic deletion.
- Supabase Storage cleanup policies apply where applicable.

---

# Compliance

Retention policies must comply with applicable legal and regulatory requirements.

---

# Core Principle

Retain only what is necessary, for as long as necessary, while ensuring legal compliance and data protection.
