from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, Enum, ForeignKey, Integer, Text

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class InventoryAdjustment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory_adjustments"

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("inventories.id"),
        nullable=False,
        index=True,
    )
    adjustment_type: Mapped[str] = mapped_column(
        Enum(
            "correction",
            "damage",
            "loss",
            "found",
            name="inventory_adjustment_type",
        ),
        nullable=False,
    )
    quantity_change: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    inventory: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="adjustments"
    )
