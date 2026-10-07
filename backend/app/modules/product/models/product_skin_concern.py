from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Product, SkinConcern


class ProductSkinConcern(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_skin_concerns"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    concern_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("skin_concerns.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="skin_concerns")
    concern: Mapped["SkinConcern"] = relationship(
        "SkinConcern", back_populates="product_skin_concerns"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "concern_id", name="uq_product_skin_concern"),
        Index("ix_product_skin_concern_pair", "product_id", "concern_id"),
    )
