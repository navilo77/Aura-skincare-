from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import JSON, UUID, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.order.models import Order

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"
    __table_args__ = ()

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        index=True,
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(
        Enum(
            "requires_payment_method",
            "requires_confirmation",
            "requires_action",
            "processing",
            "requires_capture",
            "canceled",
            "succeeded",
            name="payment_status",
        ),
        nullable=False,
        default="requires_payment_method",
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True
    )
    stripe_payment_method_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    stripe_charge_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    captured_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    failure_reason: Mapped[str | None] = mapped_column(String(512), nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="payments")
    refunds: Mapped[list["Refund"]] = relationship(
        "Refund", back_populates="payment", cascade="all, delete-orphan"
    )


class PaymentMethod(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payment_methods"
    __table_args__ = ()

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(
        Enum("card", "bank_transfer", "wallet", name="payment_method_type"),
        nullable=False,
        default="card",
    )
    stripe_payment_method_id: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    card_brand: Mapped[str | None] = mapped_column(String(50), nullable=True)
    card_last4: Mapped[str | None] = mapped_column(String(4), nullable=True)
    card_exp_month: Mapped[int | None] = mapped_column(nullable=True)
    card_exp_year: Mapped[int | None] = mapped_column(nullable=True)
    is_default: Mapped[bool] = mapped_column(nullable=False, default=False)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class Refund(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "refunds"
    __table_args__ = ()

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("payments.id"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    status: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "succeeded",
            "failed",
            "canceled",
            name="refund_status",
        ),
        nullable=False,
        default="pending",
    )
    stripe_refund_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, unique=True
    )
    reason: Mapped[str | None] = mapped_column(
        Enum("duplicate", "fraudulent", "requested_by_customer", name="refund_reason"),
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    payment: Mapped["Payment"] = relationship("Payment", back_populates="refunds")
