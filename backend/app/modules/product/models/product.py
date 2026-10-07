from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.product.models import (
        Brand,
        Category,
        ProductBenefit,
        ProductImage,
        ProductIngredient,
        ProductRoutine,
        ProductSkinConcern,
        ProductSkinType,
        ProductTag,
        ProductVariant,
    )

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Product(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "products"

    brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("brands.id"),
        nullable=False,
        index=True,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    sku: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    short_description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    description: Mapped[str | None] = mapped_column(String(4096), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("draft", "active", "archived", name="product_status"),
        nullable=False,
        default="draft",
    )
    product_type: Mapped[str] = mapped_column(
        Enum("simple", "variable", name="product_type"),
        nullable=False,
        default="simple",
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    compare_at_price: Mapped[float | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    thumbnail_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    skin_types: Mapped[list["ProductSkinType"]] = relationship(
        "ProductSkinType",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    skin_concerns: Mapped[list["ProductSkinConcern"]] = relationship(
        "ProductSkinConcern",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    ingredients: Mapped[list["ProductIngredient"]] = relationship(
        "ProductIngredient",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    benefits: Mapped[list["ProductBenefit"]] = relationship(
        "ProductBenefit",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    tags: Mapped[list["ProductTag"]] = relationship(
        "ProductTag",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    routines: Mapped[list["ProductRoutine"]] = relationship(
        "ProductRoutine",
        back_populates="product",
        cascade="all, delete-orphan",
    )
