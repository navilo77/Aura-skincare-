from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.product.models import Ingredient, Product


class ProductIngredient(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_ingredients"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    ingredient_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("ingredients.id"),
        nullable=False,
        index=True,
    )

    product: Mapped["Product"] = relationship("Product", back_populates="ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        "Ingredient", back_populates="product_ingredients"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "ingredient_id", name="uq_product_ingredient"),
        Index("ix_product_ingredient_pair", "product_id", "ingredient_id"),
    )
