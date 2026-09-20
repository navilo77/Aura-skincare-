from __future__ import annotations

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDMixin


class AdminSettings(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "admin_settings"

    key: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    value: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
