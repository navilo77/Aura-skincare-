from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Boolean, ForeignKey, Numeric

if TYPE_CHECKING:
    from app.modules.inventory.models import Supplier
    from app.modules.product.models import Product
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.inventory.models import Supplier
    from app.modules.product.models import Product

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models import Supplier
    from app.modules.product.models import Product

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class ProductSupplier(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "product_suppliers"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("suppliers.id"),
        nullable=False,
        index=True,
    )
    cost_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_preferred: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    product: Mapped["Product"] = relationship("Product")
    supplier: Mapped["Supplier"] = relationship(
        "Supplier", back_populates="product_suppliers"
    )
