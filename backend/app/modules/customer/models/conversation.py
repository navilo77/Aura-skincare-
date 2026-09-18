from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import Enum, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.customer.models import Customer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.customer.models import Customer

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class Conversation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "conversations"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("customers.id"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(
        Enum(
            "whatsapp",
            "messenger",
            "instagram",
            "website",
            name="conversation_channel",
        ),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "closed", "pending", name="conversation_status"),
        nullable=False,
        default="pending",
    )
    last_message_at: Mapped[datetime | None] = mapped_column(nullable=True)

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="conversations"
    )
