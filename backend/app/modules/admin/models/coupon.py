from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Coupon(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "coupons"

    code: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True, index=True
    )
    discount_type: Mapped[str] = mapped_column(
        Enum("percentage", "fixed", name="coupon_discount_type"),
        nullable=False,
    )
    discount_value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    min_purchase_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    max_discount_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    usage_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    used_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="true"
    )
    starts_at: Mapped[datetime] = mapped_column(nullable=False)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
