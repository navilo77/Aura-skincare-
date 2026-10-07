from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Product, Tag


class ProductTag(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_tags"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("tags.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="product_tags")

    __table_args__ = (
        UniqueConstraint("product_id", "tag_id", name="uq_product_tag"),
        Index("ix_product_tag_pair", "product_id", "tag_id"),
    )
