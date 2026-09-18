---
Document ID: SSOT-001
Title: Single Source of Truth (SSoT)
Version: 1.0
Status: Approved
Owner: Aura Skincare
Category: SSoT
Last Updated: 2026-09-15
---

# Single Source of Truth (SSoT)

## Purpose

SSoT (Single Source of Truth) হলো Aura Project-এর একমাত্র Official Data Reference।

যে তথ্য SSoT-এ থাকবে, সেটিই পুরো Project-এর জন্য সত্য (Official Truth) হিসেবে গণ্য হবে।

---

# Objective

SSoT-এর উদ্দেশ্য হলো—

- একই তথ্য একাধিক জায়গায় না রাখা।
- AI-এর বিভ্রান্তি কমানো।
- Documentation, Database এবং Code-এর মধ্যে সামঞ্জস্য বজায় রাখা।
- ভবিষ্যতে Automation সহজ করা।

---

# Core Principle

One Information

One Owner

One Official Source

---

# What Belongs in SSoT

SSoT-এ থাকবে—

- Project Information
- Business Rules
- AI Rules
- Architecture Summary
- Supported Channels
- Supported Integrations
- Feature Registry
- Requirement Registry
- API Registry
- Data Model Registry
- Document Registry

---

# What Does NOT Belong

SSoT-এ থাকবে না—

- Source Code
- SQL Script
- Prompt Text
- Long Documentation
- Meeting Notes
- Temporary Data
- Draft Content

---

# Ownership

Project Owner হলো SSoT-এর Owner।

কোনো তথ্য Owner Approval ছাড়া পরিবর্তন করা যাবে না।

---

# Update Rule

যখনই নতুন—

- Feature
- API
- Business Rule
- AI Rule
- Architecture Component

যোগ হবে,

তখন SSoT Update করতে হবে।

---

# Reference Rule

Project-এর অন্য কোনো Document একই তথ্য পুনরায় সংরক্ষণ করবে না।

সব Document প্রয়োজনে SSoT Reference করবে।

---

# AI Rule

সব AI Agent—

- Business Rule
- Supported Feature
- Project Configuration

জানার জন্য SSoT ব্যবহার করবে।

---

# Documentation Rule

Documentation আগে।

তারপর SSoT Update।

তারপর Implementation।

---

# Validation Rule

Release-এর আগে নিশ্চিত করতে হবে—

- Documentation
- SSoT
- Code

এই তিনটির মধ্যে কোনো অসামঞ্জস্য নেই।

---

# Benefits

SSoT ব্যবহারের মাধ্যমে—

- Duplicate Information কমে।
- AI Accuracy বৃদ্ধি পায়।
- Maintenance সহজ হয়।
- Documentation পরিষ্কার থাকে।
- Scaling সহজ হয়।

---

# Core Principle

If it's not in SSoT,

it's not official.