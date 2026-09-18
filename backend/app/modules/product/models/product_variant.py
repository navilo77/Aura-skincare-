from __future__ import annotations

from decimal import Decimal

import uuid

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, Numeric, String, UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product

from typing import Any

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product

from typing import Any

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class ProductVariant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_variants"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("products.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    attributes: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    product: Mapped["Product"] = relationship("Product", back_populates="variants")
