from __future__ import annotations

import uuid

from decimal import Decimal

from sqlalchemy import Enum, Numeric, String, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.order.models import BillingAddress, OrderItem, ShippingAddress
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.order.models import BillingAddress, OrderItem, ShippingAddress

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Order(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "orders"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
            name="order_status",
        ),
        nullable=False,
        default="pending",
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    order_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    shipping_address: Mapped["ShippingAddress"] = relationship(
        "ShippingAddress", back_populates="order", uselist=False
    )
    billing_address: Mapped["BillingAddress"] = relationship(
        "BillingAddress", back_populates="order", uselist=False
    )
