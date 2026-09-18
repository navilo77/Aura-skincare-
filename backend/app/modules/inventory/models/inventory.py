from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import InventoryAdjustment, InventoryMovement, InventoryReservation
    from app.modules.product.models import Product
    from app.modules.inventory.models import Warehouse
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import InventoryAdjustment, InventoryMovement, InventoryReservation
    from app.modules.product.models import Product
    from app.modules.inventory.models import Warehouse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import InventoryAdjustment, InventoryMovement, InventoryReservation
    from app.modules.product.models import Product
    from app.modules.inventory.models import Warehouse

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Inventory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventories"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True,
    )
    quantity_on_hand: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quantity_reserved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10
    )
    is_tracking_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    warehouse: Mapped["Warehouse"] = relationship(
        "Warehouse", back_populates="inventories"
    )
    movements: Mapped[list["InventoryMovement"]] = relationship(
        "InventoryMovement",
        back_populates="inventory",
        cascade="all, delete-orphan",
    )
    adjustments: Mapped[list["InventoryAdjustment"]] = relationship(
        "InventoryAdjustment",
        back_populates="inventory",
        cascade="all, delete-orphan",
    )
    reservations: Mapped[list["InventoryReservation"]] = relationship(
        "InventoryReservation",
        back_populates="inventory",
        cascade="all, delete-orphan",
    )

    @property
    def quantity_available(self) -> int:
        return self.quantity_on_hand - self.quantity_reserved
