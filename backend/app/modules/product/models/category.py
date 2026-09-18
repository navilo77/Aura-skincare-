from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Category(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "categories"

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    parent: Mapped[Category | None] = relationship(
        "Category", remote_side="Category.id", back_populates="children"
    )
    children: Mapped[list[Category]] = relationship(
        "Category", back_populates="parent"
    )
    products: Mapped[list[Product]] = relationship(
        "Product", back_populates="category"
    )
