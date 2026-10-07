from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Product, SkinType


class ProductSkinType(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_skin_types"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    skin_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("skin_types.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="skin_types")
    skin_type: Mapped["SkinType"] = relationship(
        "SkinType", back_populates="product_skin_types"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "skin_type_id", name="uq_product_skin_type"),
        Index("ix_product_skin_type_pair", "product_id", "skin_type_id"),
    )
