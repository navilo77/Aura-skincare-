from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Enum, String

if TYPE_CHECKING:
    from app.modules.customer.models import Address, Conversation
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.modules.customer.models import Address, Conversation

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Customer(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customers"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, unique=True, index=True
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "inactive", "suspended", name="customer_status"),
        nullable=False,
        default="active",
    )
    skin_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    skin_concerns: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="customer", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="customer", cascade="all, delete-orphan"
    )
