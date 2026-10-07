from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Benefit, Product


class ProductBenefit(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_benefits"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    benefit_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("benefits.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="benefits")
    benefit: Mapped["Benefit"] = relationship(
        "Benefit", back_populates="product_benefits"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "benefit_id", name="uq_product_benefit"),
        Index("ix_product_benefit_pair", "product_id", "benefit_id"),
    )
