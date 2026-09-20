from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InventoryTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    quantity_change: int
    transaction_type: str
    reference_type: str | None
    reference_id: uuid.UUID | None
    notes: str | None
    performed_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class InventoryTransactionCreate(BaseModel):
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    quantity_change: int
    transaction_type: str
    reference_type: str | None = None
    reference_id: uuid.UUID | None = None
    notes: str | None = None
    performed_by: uuid.UUID | None = None


class OrderEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_id: uuid.UUID
    event_type: str
    description: str | None
    extra_metadata: str | None
    created_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class OrderEventCreate(BaseModel):
    order_id: uuid.UUID
    event_type: str
    description: str | None = None
    extra_metadata: str | None = None
    created_by: uuid.UUID | None = None


class AutomationJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    job_type: str
    status: str
    scheduled_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    extra_metadata: str | None
    created_at: datetime
    updated_at: datetime


class AutomationJobCreate(BaseModel):
    job_type: str
    scheduled_at: datetime | None = None
    extra_metadata: str | None = None


class InventoryAlertRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    alert_type: str
    message: str
    is_resolved: bool
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime


class InventoryAlertCreate(BaseModel):
    product_id: uuid.UUID
    warehouse_id: uuid.UUID
    alert_type: str
    message: str
    is_resolved: bool = False
    resolved_at: datetime | None = None
