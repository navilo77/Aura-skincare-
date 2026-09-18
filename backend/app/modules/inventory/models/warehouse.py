from __future__ import annotations

import uuid

from sqlalchemy import Boolean, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import Inventory

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Warehouse(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "warehouses"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory",
        back_populates="warehouse",
        cascade="all, delete-orphan",
    )
