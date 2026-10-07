from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Product, RoutineType


class ProductRoutine(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_routines"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    routine_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("routine_types.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="routines")
    routine_type: Mapped["RoutineType"] = relationship(
        "RoutineType", back_populates="product_routines"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "routine_type_id", name="uq_product_routine"),
        Index("ix_product_routine_pair", "product_id", "routine_type_id"),
    )
