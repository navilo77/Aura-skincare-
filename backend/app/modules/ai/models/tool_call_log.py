from __future__ import annotations

import uuid

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class ToolCallLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_tool_call_logs"

    session_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    message_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    arguments: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("success", "error", "timeout", name="ai_tool_status"),
        nullable=False,
        default="success",
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
