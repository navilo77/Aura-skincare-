from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, UUID
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.product.models import Product

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class ProductImage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_images"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("products.id"), nullable=False, index=True
    )
    image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    alt_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product: Mapped["Product"] = relationship("Product", back_populates="images")
