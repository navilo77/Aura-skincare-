from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class InventoryTransaction(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory_transactions"

    product_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), nullable=False, index=True
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), nullable=False, index=True
    )
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_type: Mapped[str] = mapped_column(
        Enum(
            "purchase",
            "sale",
            "return",
            "adjustment",
            "reservation",
            "release",
            "transfer_in",
            "transfer_out",
            name="inventory_transaction_type",
        ),
        nullable=False,
    )
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )


class OrderEvent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "order_events"

    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("orders.id"), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "confirmed",
            "packed",
            "shipped",
            "delivered",
            "cancelled",
            "refunded",
            name="order_event_type",
        ),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), nullable=True
    )


class AutomationJob(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "automation_jobs"

    job_type: Mapped[str] = mapped_column(
        Enum(
            "inventory_sync",
            "low_stock_scan",
            "expired_reservation_cleanup",
            "order_event_processing",
            name="automation_job_type",
        ),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        Enum("pending", "running", "completed", "failed", name="automation_job_status"),
        nullable=False,
        default="pending",
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_metadata: Mapped[str | None] = mapped_column(Text, nullable=True)


class InventoryAlert(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory_alerts"

    product_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), nullable=False, index=True
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), nullable=False, index=True
    )
    alert_type: Mapped[str] = mapped_column(
        Enum(
            "low_stock",
            "out_of_stock",
            "negative_inventory",
            name="inventory_alert_type",
        ),
        nullable=False,
        index=True,
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
