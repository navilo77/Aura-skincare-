from __future__ import annotations

import uuid

from sqlalchemy import Boolean, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Brand(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")
