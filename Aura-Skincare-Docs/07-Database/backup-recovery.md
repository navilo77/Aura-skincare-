# Backup & Recovery

---

Document ID: DB-010

Title: Backup & Recovery

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines backup and recovery procedures for the Aura database platform.

---

# Backup Policy

- Supabase manages automated daily backups
- Weekly full backups via Supabase
- Monthly archive backups via Supabase

---

# Storage

- Primary Storage: Supabase Cloud
- Offsite Storage: Supabase Backup Storage

---

# Recovery Objectives

RPO: 24 Hours

RTO: 2 Hours

---

# Recovery Testing

- Quarterly restore test via Supabase
- Annual disaster recovery exercise

---

# Monitoring

Backup success and failures must be logged and alerted via Supabase monitoring.

---

# Core Principle

Backups are considered valid only after successful recovery testing.