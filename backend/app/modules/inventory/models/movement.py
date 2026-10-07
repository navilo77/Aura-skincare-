from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, ForeignKey, Integer, String, Text

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class InventoryMovement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory_movements"

    inventory_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("inventories.id"),
        nullable=False,
        index=True,
    )
    movement_type: Mapped[str] = mapped_column(
        Enum(
            "purchase",
            "sale",
            "return",
            "transfer_in",
            "transfer_out",
            "adjustment",
            name="inventory_movement_type",
        ),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    inventory: Mapped["Inventory"] = relationship(
        "Inventory", back_populates="movements"
    )
