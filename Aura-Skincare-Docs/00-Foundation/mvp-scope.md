---
Document ID: FND-003
Title: MVP Scope
Version: 1.0
Status: Approved
Owner: Aura Skincare
Category: Foundation
Last Updated: 2026-09-15
---

# MVP Scope

## Purpose

এই Document Version 1 (MVP)-এ কী তৈরি হবে এবং কী তৈরি হবে না তা নির্ধারণ করে।

যে Feature এই Document-এ নেই, তা MVP-এর অংশ হিসেবে বিবেচিত হবে না।

---

# MVP Goal

একটি স্থিতিশীল, ব্যবহারযোগ্য এবং AI-powered Beauty Commerce Platform তৈরি করা যা বাস্তব Customer-এর জন্য ব্যবহার করা যাবে।

---

# Business Scope

MVP-তে থাকবে

- Online Product Catalog
- Product Search
- Product Details
- Customer Account
- Shopping Cart
- Order Placement
- Order Tracking
- Customer Support
- Admin Dashboard

---

# AI Scope

MVP-তে থাকবে

## Customer AI

- Product Recommendation
- FAQ
- Order Status
- Basic Skin Guidance
- Customer Support
- Conversation Memory (Session)

---

## Admin AI

- Product Draft
- Product Update Suggestion
- Dashboard Assistance
- Report Summary
- Inventory Suggestion
- Business Insight

Final Approval সর্বদা Admin দেবে।

---

## Marketing AI

- Content Draft
- Facebook Content
- Instagram Content
- WhatsApp Channel Content
- TikTok Idea
- YouTube Script
- SEO Suggestion

Publish করবে না।

শুধু Draft তৈরি করবে।

---

## AI Router

AI Router সিদ্ধান্ত নেবে কোন AI Request Process করবে।

---

# Supported Channels

- Website
- WhatsApp
- Messenger

Future Ready

- Instagram DM

---

# Technology Scope

- FastAPI
- Next.js
- Supabase (Managed PostgreSQL)
- Supabase Storage
- Redis
- LangGraph
- Docker Compose
- n8n

---

# Security Scope

- Authentication
- Authorization
- Zero Trust
- Audit Logging
- Secret Management
- Human Approval

---

# Automation Scope

- Customer Support
- Marketing Workflow
- Notification
- Content Pipeline
- Order Notification

---

# Analytics Scope

- Sales Dashboard
- Customer Dashboard
- Marketing Dashboard
- AI Performance
- Business Metrics

---

# Out of Scope

Version 1-এ থাকবে না

- Kubernetes
- Microservices
- Local LLM
- Voice Assistant
- Mobile App
- Supplier AI
- Finance AI
- Inventory AI Automation
- Multi-language Support
- Autonomous Purchasing
- Automatic Product Publishing
- Automatic Refund Approval

---

# Success Criteria

MVP সফল হবে যদি—

- Customer AI অধিকাংশ সাধারণ প্রশ্নের উত্তর দিতে পারে।
- Order Process সম্পূর্ণ হয়।
- Admin AI Business-এ সহায়তা করতে পারে।
- Marketing AI Content Draft তৈরি করতে পারে।
- AI Router সঠিক Agent নির্বাচন করতে পারে।
- Human Approval System কার্যকর থাকে।

---

# Scope Change Rule

MVP Scope পরিবর্তন করতে হলে—

- Requirement তৈরি করতে হবে।
- Impact Analysis করতে হবে।
- Owner Approval নিতে হবে।
- Documentation Update করতে হবে।

Scope Change কখনও সরাসরি করা যাবে না।