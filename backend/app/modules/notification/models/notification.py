from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text, UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class NotificationTemplate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_templates"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(
        Enum(
            "email",
            "sms",
            "push",
            "whatsapp",
            "messenger",
            name="notification_channel",
        ),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class NotificationPreference(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notification_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(
        Enum(
            "email",
            "sms",
            "push",
            "whatsapp",
            "messenger",
            name="notification_channel",
        ),
        nullable=False,
    )
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Notification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("notification_templates.id"),
        nullable=True,
        index=True,
    )
    channel: Mapped[str] = mapped_column(
        Enum(
            "email",
            "sms",
            "push",
            "whatsapp",
            "messenger",
            name="notification_channel",
        ),
        nullable=False,
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "sent",
            "delivered",
            "failed",
            "cancelled",
            name="notification_status",
        ),
        nullable=False,
        default="pending",
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    sent_at: Mapped[str | None] = mapped_column(String(50), nullable=True)
