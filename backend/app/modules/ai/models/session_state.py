from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class SessionState(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_session_states"

    session_id: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    current_agent: Mapped[str] = mapped_column(
        Enum("router", "customer", "admin", "marketing", name="ai_agent_type"),
        nullable=False,
        default="router",
    )
    intent: Mapped[str | None] = mapped_column(String(100), nullable=True)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_activity_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
