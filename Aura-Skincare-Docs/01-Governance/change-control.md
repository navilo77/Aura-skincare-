---
Document ID: GOV-002
Title: Change Control
Version: 1.0
Status: Approved
Owner: Aura Skincare
Category: Governance
Last Updated: 2026-09-15
---

# Change Control

## Purpose

এই Document Aura Project-এর সকল পরিবর্তন (Change) কীভাবে পরিচালিত হবে তা নির্ধারণ করে।

এর উদ্দেশ্য হলো Documentation, Architecture এবং Business Rule-এর স্থায়িত্ব বজায় রাখা।

---

# Core Principle

পরিবর্তন করা যাবে।

কিন্তু নিয়ন্ত্রিতভাবে।

Documentation সর্বদা Code-এর আগে Update হবে।

---

# Change Categories

Aura-তে চার ধরনের Change থাকবে।

## Foundation Change

Vision, Governance, Architecture, AI Principle অথবা Core Business Rule পরিবর্তন।

এগুলো High Impact Change।

---

## Feature Change

নতুন Feature যোগ করা বা বিদ্যমান Feature পরিবর্তন।

---

## Technical Change

Database, API, Architecture, Integration অথবা Infrastructure পরিবর্তন।

---

## Documentation Change

বানান, ব্যাখ্যা, উদাহরণ অথবা Documentation Update।

---

# Change Workflow

সব Change একই Workflow অনুসরণ করবে।

Request

↓

Analysis

↓

Review

↓

Approval

↓

Implementation

↓

Documentation Update

↓

Release

---

# Change Request

যেকোনো Change-এর আগে একটি Requirement বা Change Request থাকতে হবে।

কোনো পরিবর্তন সরাসরি করা যাবে না।

---

# Impact Analysis

প্রত্যেক Change-এর জন্য নিচের বিষয়গুলো মূল্যায়ন করতে হবে।

- Business Impact
- Customer Impact
- AI Impact
- Security Impact
- Database Impact
- API Impact
- Documentation Impact

---

# Approval Rules

## Low Impact

Admin Approval যথেষ্ট।

---

## Medium Impact

Admin + Project Owner Review।

---

## High Impact

শুধুমাত্র Project Owner Approval।

---

# Documentation Rule

যদি কোনো Change Documentation-কে প্রভাবিত করে,

তাহলে Code Update করার আগে Documentation Update করতে হবে।

---

# Versioning

Major Version

Architecture অথবা Vision পরিবর্তন।

উদাহরণ

1.0 → 2.0

---

Minor Version

নতুন Feature যোগ।

উদাহরণ

1.0 → 1.1

---

Patch Version

Bug Fix বা ছোট Documentation Update।

উদাহরণ

1.1.0 → 1.1.1

---

# Deprecated Rule

যে Document আর ব্যবহার হবে না,

সেটি Delete করা যাবে না।

Status হবে

Deprecated

---

# Archived Rule

পুরনো গুরুত্বপূর্ণ Document Archive Folder-এ সংরক্ষণ করা হবে।

History কখনও মুছে ফেলা হবে না।

---

# Emergency Change

Security Issue হলে

Project Owner Documentation পরে Update করার অনুমতি দিতে পারবেন।

তবে Release-এর আগে Documentation অবশ্যই সম্পূর্ণ করতে হবে।

---

# AI Rule

AI নিজে থেকে কোনো Change Apply করতে পারবে না।

AI শুধুমাত্র—

- Analysis
- Suggestion
- Documentation Draft

তৈরি করতে পারবে।

---

# Human Rule

Final Approval সর্বদা Human দেবে।

---

# Audit Rule

সব Approved Change-এর Record সংরক্ষণ করতে হবে।

কমপক্ষে নিচের তথ্য থাকবে।

- Change ID
- Date
- Author
- Reviewer
- Approver
- Reason
- Impact
- Version

---

# Rejection Rule

Review-এ Reject হলে

কোনো Implementation করা যাবে না।

---

# Core Principle

Think First.

Review Carefully.

Approve Once.

Implement Safely.

Document Everything.