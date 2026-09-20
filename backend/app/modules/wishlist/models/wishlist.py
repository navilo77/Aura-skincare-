from __future__ import annotations

import uuid

from sqlalchemy import UUID, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Wishlist(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "wishlists"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), nullable=False, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    items: Mapped[list["WishlistItem"]] = relationship(
        "WishlistItem", back_populates="wishlist", cascade="all, delete-orphan"
    )


class WishlistItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "wishlist_items"

    wishlist_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("wishlists.id"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )
    product_variant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
    )

    wishlist: Mapped["Wishlist"] = relationship("Wishlist", back_populates="items")
