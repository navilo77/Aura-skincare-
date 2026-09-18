# Indexing Strategy

---

Document ID: DB-005

Title: Indexing Strategy

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines the indexing strategy for performance and scalability.

---

# Primary Indexes

Every primary key is indexed automatically.

---

# Foreign Key Indexes

Required for:

- customer_id
- order_id
- product_id
- category_id

---

# Search Indexes

Recommended for:

- product_name
- category_name
- email
- phone_number

---

# Composite Indexes

Examples

(customer_id, created_at)

(order_id, product_id)

(product_id, category_id)

---

# Full-Text Search

Future implementation:

- Product descriptions
- AI conversation history
- Knowledge Base

---

# Monitoring

Indexes should be reviewed periodically using Supabase (Managed PostgreSQL) performance statistics.

---

# Rules

- Avoid duplicate indexes.
- Remove unused indexes.
- Create indexes only for frequent query patterns.
- Measure performance before adding indexes.

---

# Core Principle

Indexes optimize read performance without unnecessarily increasing write overhead.