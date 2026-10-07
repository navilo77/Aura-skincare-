from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UUID, DateTime, Enum, ForeignKey, Integer

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class InventoryReservation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory_reservations"

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("inventories.id"),
        nullable=False,
        index=True,
    )
    order_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("order_items.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(
            "reserved",
            "released",
            "fulfilled",
            "cancelled",
            name="inventory_reservation_status",
        ),
        nullable=False,
        default="reserved",
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    inventory: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="reservations"
    )
