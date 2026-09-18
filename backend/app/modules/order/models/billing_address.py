from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.order.models import Order
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.order.models import Order

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class BillingAddress(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "billing_addresses"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address_line1: Mapped[str] = mapped_column(String(255), nullable=False)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="billing_address")
