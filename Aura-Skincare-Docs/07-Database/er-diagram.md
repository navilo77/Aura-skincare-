# Entity Relationship Diagram

---

Document ID: DB-002

Title: Entity Relationship Diagram

Version: 1.0

Status: Approved

Owner: Aura Skincare

Category: Database

  Last Updated: 2026-09-17

---

# Purpose

This document defines the logical relationships between all primary database entities.

---

```mermaid
erDiagram

CUSTOMERS ||--o{ CUSTOMER_ADDRESSES : has
CUSTOMERS ||--o{ CONVERSATIONS : starts
CUSTOMERS ||--o{ ORDERS : places

PRODUCT_CATEGORIES ||--o{ PRODUCTS : contains

PRODUCTS ||--|| INVENTORIES : owns

ORDERS ||--o{ ORDER_ITEMS : contains

PRODUCTS ||--o{ ORDER_ITEMS : referenced_by

ORDERS ||--|| SHIPPING_ADDRESSES : ships_to

ORDERS ||--|| BILLING_ADDRESSES : bills_to

ORDERS ||--o{ PAYMENTS : has

CONVERSATIONS ||--o{ RECOMMENDATIONS : generates

PRODUCTS ||--o{ RECOMMENDATIONS : suggested_in

CUSTOMERS {
  uuid customer_id
  string full_name
  string email
  string phone
  string status
  string skin_type
  json skin_concerns
}

CUSTOMER_ADDRESSES {
  uuid address_id
  uuid customer_id
  string address_line1
  string city
  string country
}

CONVERSATIONS {
  uuid conversation_id
  uuid customer_id
  string channel
  string status
}
```

---

# Relationship Rules

- One Customer → Many Orders
- One Customer → Many Conversations
- One Category → Many Products
- One Product → One Inventory
- One Order → Many Order Items
- One Order → One ShippingAddress
- One Order → One BillingAddress
- One Conversation → Many Recommendations

---

# Core Principle

Relationships must enforce data integrity through foreign keys.