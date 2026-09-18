# Database Naming Conventions

---

Document ID: DB-004

Title: Database Naming Conventions

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

Last Updated: 2026-09-15

---

# Purpose

Defines the official naming standards for all database objects.

---

# Tables

Format

snake_case

Examples

customers

orders

order_items

product_categories

---

# Columns

snake_case

Examples

customer_id

created_at

updated_at

deleted_at

---

# Primary Keys

<entity>_id

Examples

customer_id

product_id

order_id

---

# Foreign Keys

<referenced_entity>_id

Examples

customer_id

product_id

category_id

---

# Indexes

idx_<table>_<column>

Example

idx_products_category_id

---

# Unique Constraints

uq_<table>_<column>

Example

uq_customers_email

---

# Foreign Key Constraints

fk_<table>_<referenced_table>

Example

fk_orders_customers

---

# Check Constraints

chk_<table>_<rule>

Example

chk_products_price

---

# Core Principle

Consistent naming improves readability, maintainability, and automation.