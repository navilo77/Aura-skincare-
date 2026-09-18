from __future__ import annotations

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class MfaSecret(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "mfa_secrets"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID[uuid.UUID](as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    secret: Mapped[str] = mapped_column(String(255), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    backup_codes: Mapped[str | None] = mapped_column(String(255), nullable=True)
